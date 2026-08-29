# Platform Pack — the contract

Every file in `.kiro/platforms/` answers the same seven questions, under the same headings, in this order.
A skill loads a pack knowing exactly which headings it will find, so it never searches and never guesses.

**To add a platform:** copy this file, fill every section, then add a row to
`.kiro/steering/project-config.md` § Platforms. No skill is edited.

A pack is loaded only when its platform is enabled in that table. A project that disables a platform never
pays for its pack.

---

## Targets

The platform ids this pack serves, and the driver rule each one uses. One pack may serve several ids that
differ only in viewport or OS.

## Target grammar

What `id=`, `desc=` and `text=` resolve to on this platform, and the resolution order. State explicitly that
no coordinate is ever written into a plan, and name the one rule that governs the exception if the driver
has one.

## Observables

The exhaustive list of things an assertion may be tied to on this platform. This list is the contract: an
assertion that cannot tie to an entry here goes back to classification, and is never weakened to fit.

Where a depth level the design phase asks for is not directly observable, say what it becomes instead.

## Unaddressable elements

How common they are here, and the exact fix to ask for — the attribute, and which team owns it.

## Label overlay

Available, or not. This decides whether one frame can carry several labelled checkpoints, or whether a
capture is attributed by its file name alone.

## State reset

Every reset this platform offers, in ascending cost, each written as the action a wave states. A wave picks
the lightest one that reaches its first precondition.

## Preflight

What must be confirmed before the first wave, and where each value comes from. Include how to read the build
under test, and say `unknown` is acceptable when the platform exposes none.
