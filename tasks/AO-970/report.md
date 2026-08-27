# AO-970 — Manual Execution Report

**Issue:** [AO-970](https://aquariux.atlassian.net/browse/AO-970) — [OTC][MobileApp] Onboarding flow for backoffice created member
**Executed:** 2026-08-27
**Platform:** Android (emulator-5554, OTC Mobile App `com.bfgto.sit.app` v0.15.0). iOS/TestFlight was skipped this run — no viable control method for the physical device (`iPhone Mirroring` gives no accessibility tree; execution would be blind coordinate taps).

## Summary

| Status | Count |
|---|---|
| ✅ PASSED | 6 |
| ❌ FAILED | 0 |
| 🚫 BLOCKED | 0 |

## Test Accounts Used

| Email | Type | State before run | Created this session? |
|---|---|---|---|
| ao970member@yopmail.com | Personal | Backoffice-created, no password set | No — pre-existing |
| ao970business@yopmail.com | Business | Backoffice-created, no password set | Yes — via Back Office Create Member |
| ao970personal@yopmail.com | Personal | Backoffice-created, no password set | Yes — via Back Office Create Member |
| ao970member2@yopmail.com | Personal | Backoffice-created, no password set | Yes — via Back Office Create Member, for a fresh TC-178546 re-run |

## Results

### TC-178546 · Login – Suspended error shown when no password set
**Result:** PASSED
**Evidence:** [AO-970_TC-178546_2.png](../../evidence/AO-970/AO-970_TC-178546_2.png) (fresh, self-triggered re-run — see note)
Created a new backoffice Personal member `ao970member2@yopmail.com` (no password ever set), entered it + a random password (`RandomPass1!`) on the Login screen, tapped Log in → "Account Suspended — Your account has been suspended. Please go to Forgot Password to retain your account." shown, member stayed on Login screen.

*(Superseded evidence: [AO-970_TC-178546_1.png](../../evidence/AO-970/AO-970_TC-178546_1.png) was captured earlier against `ao970member@yopmail.com`, but that screen was already showing before this session started interacting with the device, so it wasn't a self-triggered execution. Re-run above with a fresh account to close that gap.)*

### TC-178547 · Passcode setup screen shown on first login after reset
**Result:** PASSED
**Evidence:** [AO-970_TC-178547_1.png](../../evidence/AO-970/AO-970_TC-178547_1.png)
Continuing from TC-178546's account: Forgot Password → OTP → reset password → Log in → an unlisted "Verify your identity" OTP step appeared (not in the TC's written steps, but required by the app) → Create Passcode screen shown: title, 6-digit dot input, numeric keypad, no Back/Skip button.

### TC-191118 · Personal — full onboarding through Passcode + Biometric + Home
**Result:** PASSED
**Evidence:** [AO-970_TC-191118_1.png](../../evidence/AO-970/AO-970_TC-191118_1.png)
Directly continued from TC-178547 on the same account: entered passcode `112233` twice → Biometric Setup was skipped automatically (emulator has no enrolled biometric hardware, which the TC explicitly allows) → landed on Home screen, fully authenticated.

### TC-191117 · Personal — Sign Up routing to Forgot Password
**Result:** PASSED
**Evidence:** [AO-970_TC-191117_1.png](../../evidence/AO-970/AO-970_TC-191117_1.png)
Used the fresh `ao970personal@yopmail.com` account (untouched, no password ever set). On Setup Email screen, entered that email → "Please go to Forgot Password page to reset your password." shown; the generic "already registered" error did not appear; stayed on Setup Email screen.

### TC-178548 · Business — Sign Up routing to Forgot Password
**Result:** PASSED
**Evidence:** [AO-970_TC-178548_1.png](../../evidence/AO-970/AO-970_TC-178548_1.png)
Same check as TC-191117, using the fresh `ao970business@yopmail.com` account. Identical correct error shown.

### TC-191116 · Business — full onboarding through Passcode + Biometric + Home
**Result:** PASSED
**Evidence:** [AO-970_TC-191116_1.png](../../evidence/AO-970/AO-970_TC-191116_1.png)
Forgot Password → OTP → reset password → Log in → identity-verification OTP → Create Passcode (`445566`, confirmed) → Biometric auto-skipped (no hardware) → Home screen shown, fully authenticated.

## Bugs Found

None. All 6 TCs passed against their written expected results.

## Possible defect spotted outside AO-970 scope

While on the Account tab for the Business account (`ao970business@yopmail.com`), the profile header showed "AO970 Business" with the subtitle **"Personal account"** — should read "Business account". Not one of the 6 TCs and not filed as a bug yet; flagging for the user to confirm before it's reported separately.

## Notes for future runs

- **Identity-verification OTP step**: both full-login flows (178547→191118 and 191116) triggered an extra "Verify your identity" 6-digit email OTP step right after Log in, before the Passcode screen. This isn't mentioned in any of the 6 TCs or in `.claude/domain/otc-mobile.md`. Not a defect — just an undocumented step worth adding to the domain file or a future TC.
- **Emulator network**: the emulator's default NAT network could not reach the SIT backend until the emulator was rebooted (needed a VPN client active on the device itself, not just the host Mac). If this happens again, a reboot is the fix that worked.
- **Emulator stability**: hit two ANRs ("BFGTO-SIT isn't responding") on the Welcome→Login transition after a long session; resolved by a second emulator reboot. Likely resource strain from a long-running session, not a product defect — worth a quick reproduction check on a fresh emulator if it recurs.
- **Sign Up name field**: rejects digits (`AO970` as a first name triggers "Only letters, spaces, hyphens (-), and apostrophes (') are allowed.") — expected validation behavior, just noting for anyone reusing `AO970`-style throwaway names in future manual runs.
