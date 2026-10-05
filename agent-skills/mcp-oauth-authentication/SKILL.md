---
name: mcp-oauth-authentication
description: Authenticate remote MCP and agent tools with OAuth while keeping credentials outside skill definitions and enforcing explicit authorization boundaries.
---

# MCP OAuth Authentication

Use OAuth for remote MCP authentication without placing credentials in skill files, prompts, or generated artifacts. Separate authentication from authorization, validate issuer/resource/audience/scopes and redirect policy, use approved PKCE/client flows, keep tokens in the runtime credential store, and fail closed on expiry or invalid authorization. Authentication never grants arbitrary tool permissions.

## Verification
Verify identity, granted scopes, authorized tool access, token-expiry handling, and absence of secrets in logs and generated artifacts.
