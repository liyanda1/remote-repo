---
id: ota.scn.power-loss-recovery
slot: intent
domain: ota
title: 刷写中断电后恢复
status: confirmed          # draft | proposed | confirmed | disputed
confidence: certain
source: user-answer
source_ref: "conversation:2026-11-08#3"
tags: [回滚, 上电自检]
links:
  - { to: ota.st.flashing_power_lost, type: composed_of, weight: 1.0 }
  - { to: ota.st.boot_rollback_check, type: composed_of, weight: 0.8 }
  - { to: ota.scn.failed-rollback,    type: fulfills,    weight: 0.3 }
evidence:
  - { ref: "docs/ota-design.md#L118-L140", note: 设计文档 4.2 节 事务恢复流程 }
  - { ref: "test/power_loss_test.cpp#L22", note: UT 里已有对应用例 }
updated: 2026-11-08
---

## 一句话
刷写过程中整车断电，重新上电后系统必须能自行回到可用状态，不允许变砖。

## 前置条件
- 升级处于 `FLASHING` 阶段
- A/B 分区已写入但尚未激活

## 预期行为
1. 上电自检读取事务标记，发现未完成事务
2. 校验 B 分区镜像签名
3. 签名有效 → 激活 B 分区；无效 → 回滚到 A 分区
4. 向云端上报 `3042`（刷写中断，已恢复）

## 边界与坑
- **电量不足时不允许重试**，避免二次变砖
- 断电点位若在 `erase` 之后 `write` 之前，事务标记可能未落盘，依赖 bootloader 兜底

## 关联
- 机制：[[ota.st.flashing_power_lost]]、[[ota.st.boot_rollback_check]]
- 用例：[[ota.test.power_loss_recovery]]
- 代码：`RollbackMgr::recover()`、`FlashState::persist()`
- 上下游：[[uds.svc.seq_0x31_erase]]

## 待确认
- 上报码 3042 是否与服务端约定一致？（gap: G-20261108-03）
