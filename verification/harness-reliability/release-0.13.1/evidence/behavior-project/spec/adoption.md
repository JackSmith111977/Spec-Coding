# 受控候选测试接入基线

## 声明意图

仅本地 user + Agent 使用；工作语言中文；流程产物只在本地授权测试空间保存，不进入团队共享或发布边界。

## 稳定绑定

目标为 `<repo>/.harness-build/patch-0.13.1/behavior-project` 合成项目。Spec Workspace 为目标内 `spec/`，总入口为 [README.md](README.md)。

## 约束

仅执行用户指定验证队列，不建立真实产品需求。只读取固定候选包、授权合成项目及当前 runtime 必要能力；不读取 Canonical 源码、其他测试成绩或 Oracle，不联网、不委派、不修改冻结包、不安装、不改全局配置、不进行 Git 推送。测试记录不作为正式发行证明。
