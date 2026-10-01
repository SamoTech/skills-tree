# Post-P2.2 Capability Runtime Audit — 2026-10-02

## Finding

`CapabilityRuntime` already existed as a read-only deterministic runtime with focused regression tests, but `UniversalRegistry` had no typed Capability facade. Consumers could either traverse raw registry storage or instantiate the separate runtime, leaving an inconsistent abstraction boundary.

## Selected vertical slice

Integrate the existing `CapabilityRuntime` into `UniversalRegistry` and expose `resolve_capability()`, `implementations_for_capability()`, and `adapters_for_capability()`.

## Contract boundary

No new Capability, Implementation, Adapter, compatibility, provider, platform, framework, model, protocol, runtime, evidence, or graph facts are introduced. Existing validated relationships are reused. The import cycle is avoided by keeping the `UniversalRegistry` type import in `registry/capability.py` under `TYPE_CHECKING`.

## Verification

PR #236 exact head `ccc0902bcb87714c8709d9a8f5d6d100554edb2f` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `8fc4dc8f6423b6b39ec2218f077a9d153b4560da`.

**Status:** VERIFIED.
