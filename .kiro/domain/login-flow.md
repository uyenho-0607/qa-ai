---
inclusion: manual
---

# BFG OTC App — Login Flow (runbook; Android verified)

Source: live walk-through on an Android emulator, 2026-08-26.
Build: `app-release.apk`, package `com.bfgto.sit.app`, versionName 0.15.0 (versionCode 1),
minSdk 24 / targetSdk 36. React Native + Expo (SDK 57), Hermes, bridgeless.
Device: AVD `pixel6` — Android 15 (SDK 35), 1080x2400, density 420.

This is the **operational** side: how to actually get logged in on a device, and what bites.
The product **spec** for Login — rules, error strings, lockout limits, statuses — lives in
`otc-mobile.md` § Login. Do not duplicate it here.

A runbook, not a spec index: prose and commands, like `flows.md` — not the one-fact-per-line
`#tag` format of `otc-mobile.md` / `otc-shared.md`. The atomic facts are mirrored as tags under
**Quick facts** so they stay greppable; everything else needs its explanation to be usable.

Locators: `.kiro/locator-cache.json` → `bfg-otc-app`. Identifiers live under `screens`
(platform-neutral — an RN `testID` is the same string on all three platforms); Android's
coordinates and commands sit under `android`. `ios` and `web` are stubs listing what is
needed to fill them.

OTP retrieval: `scripts/mailinator_otp.py`.

**Platform scope.** The app ships Android + iOS + web from one RN codebase, but only
**Android** has been walked. The flow, the screen order, the setup steps and the OTP handling
should hold on iOS and web; the coordinates, `adb`/`pm clear` commands and keyevents will not.
iOS and web sections are still to be written — see `bfg-otc-app.ios._needed` / `.web._needed`
for what each requires.

> Everything below is observed on build 0.15.0. Where the live app differs from what
> `otc-mobile.md` records, it is marked **⚠ DEVIATION**.

---

## Quick facts

Tags: `#device` `#setup` `#creds` `#otp` `#launch` `#gotcha` `#scope`

#device  Boot | `emulator -avd pixel6`, backgrounded | the `mobile` server does NOT boot an AVD
#device  AVD | use `pixel6` | `pixel7pro` also exists and voids every cached coordinate
#device  Install | `app-release.apk` at repo root | a fresh/wiped AVD has no app installed
#setup   Env gate | `aq@aq.com` | one-time per INSTALL | fresh install only | reset: `adb shell pm clear com.bfgto.sit.app`
#setup   App passcode | `111111` | one-time per DEVICE | first login on that device | entered twice (Create → Confirm)
#creds   Mobile app account (works on office network) | `mth2608@mailinator.com` / `SHARED_PASSWORD`
#creds   `MEMBER_APP_BUSINESS` | `mth2107@yopmail.com` | UNUSABLE here — yopmail blocked on office network
#otp     Login OTP | 6 digits | sender `aqxotc-sit@s20ip12.com` | subject "BFG OTC Verification Code" | valid 5 min | resend after 60s
#otp     Fetch | `.venv/bin/python scripts/mailinator_otp.py otp mth2608 --after now --sender aqxotc-sit`
#launch  Android | `adb shell am start -n com.bfgto.sit.app/com.bfgtoapp.MainActivity` | `monkey` does NOT work (exits -5)
#gotcha  Splash hangs forever | corrupt okhttp DiskLruCache after unclean shutdown | fix: `pm clear`
#gotcha  yopmail | all domains + mirrors blocked on office network (80 and 443) | use mailinator or mail.tm
#gotcha  Button labels | login form CTA is "Log in"; Welcome screen CTA is "Login" | exact-text locators hit the wrong screen
#scope   Env gate + passcode | install/device setup, NOT login steps | keep out of login TCs

---

## Device bring-up

Cold machine to a running app. This precedes everything below.

`mobile_list_available_devices` lists devices **already** connected — it does not boot an AVD.
Booting is a shell step, and it comes first. There is no `mobile_use_device`: every `mobile_*`
call takes the `device` id explicitly.

**Use `pixel6`.** Every coordinate in the cache was measured on it at 1080x2400.
`pixel7pro` exists on this machine and voids all of them.

```bash
# 1. boot — run this in the background; the emulator process never returns
emulator -avd pixel6

# 2. wait for it — `am start` or a mobile_* call against a booting device fails "device offline".
#    The sleep runs inside the device shell, so it does not block the host.
adb wait-for-device shell 'while [ -z "$(getprop sys.boot_completed)" ]; do sleep 1; done'
```

Then, over the `mobile` server:

1. `mobile_list_available_devices` — take the id (`emulator-5554` with one emulator up).
2. `mobile_list_apps` — is `APP_PACKAGE` there? A fresh or wiped AVD does not have it.
3. Absent → `mobile_install_app`, `path` = `app-release.apk` at the repo root (build 0.15.0).
4. `mobile_launch_app`. Pass `locale` wherever a TC asserts on visible text.

A **fresh install lands on the env gate**, not Welcome — the one-time setup steps below apply.
Raw `adb` remains the fallback and is what the walkthrough below is written in; the launch
command is `android.launch` in the cache, and `monkey` does not work.

---

## The flow

```
install → launch → Splash (Bond Financial Group)
  → [SETUP, fresh install only]  Env gate: aq@aq.com → Login
  → Welcome: Login | Sign Up
  → Login form: email + password → Log in
  → Verify your identity: 6-digit email OTP
  → [SETUP, first login per device]  Create passcode 111111 → Confirm 111111
  → Home
```

Steps marked `[SETUP]` are one-time. The recurring login path is just:

```
launch → Splash → Welcome → Login form → OTP → Home
```

Two steps are **one-time setup**, not part of the per-login path. Neither reappears on a
normal login, so do not build them into login TCs — they belong to install/device setup.

| Setup step | Value | Scope | When it appears | How to get it back |
|---|---|---|---|---|
| Env gate | `aq@aq.com` | per **install** | fresh install only | `adb shell pm clear com.bfgto.sit.app` |
| Create passcode | `111111` | per **device** | first login on that device | log in as a different account, or `pm clear` |

- **Env gate — `aq@aq.com`, fresh install only.** A SIT environment unlock, entered once. It
  survives logout and re-login; reinstalling over the top does not bring it back, only clearing
  app data does.
- **Create passcode — `111111`, per device.** Use `111111` on every device unless a test says
  otherwise. Asked once, on the first login on that device, and confirmed twice
  (`Create passcode` → `Confirm your passcode`). It is device-local — a second device, or a
  cleared one, asks again and gets `111111` again. Logging in as a *different* account on the
  same device also re-triggers it (see `otc-mobile.md` `#rule Account switch on device`).

Logout returns to **Welcome** — past the env gate, and with the passcode still enrolled.

---

## Deviations from `otc-mobile.md` § Login

- **⚠ DEVIATION — env gate is undocumented.** `#flow Login` records
  `Splash → Biometric/Passcode unlock OR Email+Password → Home`. It has no env gate. The gate
  is a SIT build artefact, not product behaviour, and is worth keeping out of TCs.
- **⚠ DEVIATION — login sends an email OTP.** `#scope Login — out of scope (phase 1)` lists
  "OTP login" as out of scope, but 0.15.0 requires a 6-digit email OTP on every
  email+password login. Confirm with the team whether the spec or the build is behind.
- **⚠ DEVIATION — button label.** `#screen Login` says CTA `Login`. The actual login-form
  button reads **`Log in`** (two words). `Login` is the *Welcome* screen's button. Both exist,
  one screen apart — an exact-text locator will hit the wrong one.
- **No biometric prompt** on this emulator (no enrolled biometric). Passcode is the only
  local unlock path here.

---

## Driving it over adb

`adb -s emulator-5554`. Launch explicitly — `monkey` fails to start this package:

```bash
adb shell am start -n com.bfgto.sit.app/com.bfgtoapp.MainActivity
```

Read the screen. uiautomator surfaces a testID as `resource-id` with no package prefix:

```bash
adb shell uiautomator dump /sdcard/ui.xml && adb shell cat /sdcard/ui.xml
```

Typing: `input text` handles `@` and `!` unescaped, so `Te5t1ng!` goes in as-is (quote it in
the shell). After each field, `input keyevent KEYCODE_BACK` dismisses the keyboard.

### Getting the OTP

Mailinator public inboxes need no key. **Take the cutoff before triggering the mail** — the
inbox keeps old codes and you will otherwise submit a stale one:

```bash
CUTOFF=$(python3 -c "import time;print(int(time.time()*1000))")
# ...tap Log in...
.venv/bin/python scripts/mailinator_otp.py otp mth2608 --after "$CUTOFF" --sender aqxotc-sit
```

Sender is `aqxotc-sit@s20ip12.com`, subject `BFG OTC Verification Code`, **valid 5 minutes**.
Resend is locked behind a 60s countdown.

Entering it: the six `otp-cell-{n}` nodes are **not clickable**. Tap cell 0 to focus the hidden
input, then send all six digits in one `input text` — they auto-advance and the screen
self-submits on the sixth.

---

## Things that will waste your afternoon

- **`monkey` cannot launch this app.** It exits `-5` with no error. Use `am start` with
  `com.bfgto.sit.app/com.bfgtoapp.MainActivity`.
- **Splash hangs forever after an unclean shutdown.** Symptom: orange Bond Financial Group
  splash, minutes, no crash in logcat. Cause is a corrupt okhttp cache —
  `W okhttp.OkHttpClient: DiskLruCache /data/.../files/okhttp is corrupt`. Fix:
  `adb shell pm clear com.bfgto.sit.app`. Costs you the env gate and the passcode, not the account.
- **yopmail is blocked on the office network.** Every domain and mirror times out on both 80
  and 443; it is not a sandbox or DNS problem. Use mailinator. `scripts/mailtm_otp.py` (mail.tm)
  is the other option.
- **The emulator can die on app launch.** The qemu process itself exits, so adb reports no
  devices rather than an offline one. Check with `pgrep -fl qemu` before debugging adb;
  reboot with `emulator -avd pixel6`.
- **`desc=Log out` matches two nodes** once the confirm sheet is open — the menu row and the
  sheet button. Disambiguate by y.
- **An `EditText`'s `text` is the placeholder while empty**, the typed value once filled. To
  clear a field: tap it, `KEYCODE_MOVE_END`, then N × `KEYCODE_DEL`.

---

## Test account used

`MEMBER_APP_BUSINESS` in `project-config.md` is `mth2107@yopmail.com`, which is unreachable
from the office network. The working account on this build:

| Field | Value |
|---|---|
| Email | `mth2608@mailinator.com` |
| Password | `SHARED_PASSWORD` |
| App passcode | `111111` — the standing default, set per device |
| Display name | bun bo — "Personal account" |
| Balance | $0.00, Everyday account, 4 currencies, no transactions |

The passcode is not an account credential — it is enrolled per device, so a new or cleared
device asks for it again. Set it to `111111` every time.
