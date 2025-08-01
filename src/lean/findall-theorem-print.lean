import Lean
import Mathlib

open Lean
open Lean.Elab
open Lean.Elab.Command
open Lean.Meta
open Lean.Parser


/-!
### 函数定义部分
这是三个独立的、可复用的顶层函数。
-/

/--
查找环境中的定理。

- `env`: 要搜索的环境
- `limit`: 返回定理的最大数量
- `filter`: 一个应用于定理名称的过滤器函数
- **返回**: 一个包含定理名称和信息的数组
-/
def findThms (env : Environment) (limit : Nat) (filter : Name → Bool) : Array (Name × ConstantInfo) := Id.run do
  let mut thms := #[]
  for (name, cinfo) in env.constants.toList do
    if thms.size >= limit then
      break
    match cinfo with
    | ConstantInfo.thmInfo .. =>
      if filter name then
        thms := thms.push (name, cinfo)
    | _ => continue
  return thms

/--
将定理列表打印到 Lean InfoView。

- `thms`: 要打印的定理数组
- `limit`: 用于在日志消息中显示原始限制
-/
def logThms (thms : Array (Name × ConstantInfo)) (limit : Nat) : CommandElabM Unit := do
  if thms.isEmpty then
    logInfo m!"[find_thms] no matching theorems found"
  else
    logInfo m!"[find_thms] displaying {thms.size} theorems (limit: {limit}, internal proofs excluded)"
    for (name, info) in thms do
      let ConstantInfo.thmInfo val := info | continue
      logInfo m!"{name}:\n{val.type}"


/--
将定理列表美化后写入到指定文件。

- `thms`: 要写入的定理数组
- `filePath`: 输出文件的路径
-/
def writeThmsToFile_raw (thms : Array (Name × ConstantInfo)) (filePath : System.FilePath) : CommandElabM Unit := do
  let mut content := ""
  for (name, info) in thms do
    let ConstantInfo.thmInfo val := info | continue
    content := content ++ s!"{name} :\n{val.type}\n\n===================\n\n"

  IO.FS.writeFile filePath content
  logInfo m!"[find_thms] Exported {thms.size} theorems to {filePath}"

def writeThmsToFile (thms : Array (Name × ConstantInfo)) (filePath : System.FilePath) : CommandElabM Unit := do
  -- 使用 `runTermElabM` 创建一个可以安全执行 MetaM 操作的上下文
  let content ← runTermElabM fun _ => do
    -- 这个 do 块现在在 TermElabM 中，可以直接 `await` MetaM 的操作
    withOptions (fun o => o.setBool `pp.universes false |>.setBool `pp.notation true) do
      let mut lines : Array String := #[]
      for (name, info) in thms do
        let ConstantInfo.thmInfo val := info | continue
        -- 在这里不再需要 liftMetaM，可以直接执行
        let typeFmt ← PrettyPrinter.ppExpr val.type
        lines := lines.push s!"{name} :\n\n{typeFmt.pretty}\n\n=======================\n\n"
      return String.join lines.toList

  IO.FS.writeFile filePath content
  logInfo m!"[find_thms] Exported {thms.size} theorems to {filePath}"


/-!
### 命令定义部分
Lean 命令现在只负责解析参数和协调调用上面的函数。
-/

syntax (name := findAllThms) "#find_all_thms" (num)? : command
syntax (name := findAllThmsWithoutPrefix) "#find_all_thms_without_prefix" (num)? : command
syntax (name := findAllThmsWithPrefix) "#find_all_thms_with_prefix" (num)? : command

@[command_elab findAllThms]
def elabFindAllThms : CommandElab := fun stx => do
  -- 1. 解析参数
  let limit : Nat :=
    let optLimit : Option Nat := do
      let numStx ← Syntax.getOptional? (stx.getArg 1)
      numStx.isNatLit?
    optLimit.getD 10

  -- 2. 定义本次查询所用的过滤器
  let filter (nm : Name) : Bool :=
    ¬ nm.isInternal

  -- 3. 调用核心函数获取数据
  let env ← getEnv
  let theorems := findThms env limit filter

  -- 4. 调用处理函数来展示和保存结果
  logThms theorems limit
  writeThmsToFile theorems "found_theorems.txt"



@[command_elab findAllThmsWithoutPrefix]
def elabFindAllThmsWithoutPrefix : CommandElab := fun stx => do
  -- 1. 解析 limit 参数
  let limit : Nat :=
    let optLimit : Option Nat := do
      let numStx ← Syntax.getOptional? (stx.getArg 1)
      numStx.isNatLit?
    optLimit.getD 10

  -- 2. 解析可选的前缀列表
  let prefixes : List String := [
    "Mathlib", "Lean",
    "CategoryTheory", "Asymptotics"
    ]

  -- 3. 定义过滤器
  let filter (nm : Name) : Bool :=
    let nameStr := nm.toString
    if nm.isInternal then
      false
    else
      prefixes.isEmpty || ¬ (prefixes.any fun p => nameStr.startsWith p)

  -- 4. 获取数据和处理
  let env ← getEnv
  let theorems := findThms env limit filter

  logThms theorems limit
  writeThmsToFile theorems "found_theorems_without_prefix.txt"


@[command_elab findAllThmsWithPrefix]
def elabFindAllThmsWithPrefix : CommandElab := fun stx => do
  -- 1. 解析 limit 参数
  let limit : Nat :=
    let optLimit : Option Nat := do
      let numStx ← Syntax.getOptional? (stx.getArg 1)
      numStx.isNatLit?
    optLimit.getD 10

  -- 2. 解析可选的前缀列表
  let prefixes : List String := [
    "Nat.", "Real.", "Int.",
    "Finset.", "Set."
    ]

  -- 3. 定义过滤器
  let filter (nm : Name) : Bool :=
    let nameStr := nm.toString
    if nm.isInternal then
      false
    else
      prefixes.isEmpty || (prefixes.any fun p => nameStr.startsWith p)

  -- 4. 获取数据和处理
  let env ← getEnv
  let theorems := findThms env limit filter

  logThms theorems limit
  writeThmsToFile theorems "found_theorems_with_prefix.txt"




#find_all_thms 100
#find_all_thms_with_prefix 100
#find_all_thms_without_prefix 100
