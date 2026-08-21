# qa-ai — Questions and Answers

qa-ai is an assistant for manual QA work. Give it a ticket number in plain English and it writes test cases,
files bugs with evidence, and verifies fixes — working directly in Jira, Testmo and Figma, and asking before it
saves anything. Every answer below stands on its own, so you can jump straight to any question.

## What is qa-ai?

qa-ai is a QA assistant that already knows this team's QA rules — how a test case should be named, what a bug
report must contain, and which folder each file belongs in. You give qa-ai a Jira ticket number and describe
what you want in plain English. qa-ai does the work and shows you the result before saving anything. You do
not need to understand how qa-ai works internally in order to use it.

qa-ai can write test cases for a ticket, report a bug in Jira, check whether a fix worked, apply a reviewer's
feedback to your test cases, build an evidence document and place your screenshots in it, explore the
application and record how it behaves, and save your work for the team to review.

## Do I need to be technical to use qa-ai?

No. You do not need to write code or understand the internals to use qa-ai. You type what you want in plain
English, such as "I need test cases for AO-306" or "I found a bug", and qa-ai chooses the right tool. You do
need to run one setup command in the Terminal the first time you use qa-ai on a new laptop.

## What are the three most important things to know about qa-ai?

First, qa-ai asks before it saves. You always see what qa-ai created before it becomes real.

Second, you can stop qa-ai at any time. If you come back later and say the same thing again, qa-ai picks up
where it left off instead of starting over. Nothing is lost when you interrupt a job.

Third, qa-ai will not make things up. If qa-ai needs a link, a password, a ticket number, or an expected
result that it does not have, qa-ai stops and asks you for it rather than inventing a plausible value.

## How do I set up qa-ai on a new laptop?

Setting up qa-ai takes one command. Open the Terminal, go to the qa-ai project folder, and run the onboarding
wizard by typing `./onboarding.sh` and pressing Enter. The wizard walks you through every setting and asks you
for each password or key as it needs it.

The onboarding wizard asks "do you already have this?" for each key. If you say yes, the wizard skips the
explanation and goes straight to letting you paste the value. Anything already set up on your laptop is
detected and left alone. It is safe to quit the wizard halfway through with Ctrl-C and run it again later,
because it only fills in the gaps.

If you want to see what the onboarding wizard would do without changing anything on your laptop, run
`./onboarding.sh --test` instead. That is a dry run: it writes nothing and opens no browser tabs.

## Should I ask the assistant to run the setup wizard for me?

No. You must run the onboarding wizard yourself, in your own Terminal. The wizard waits for you to type
passwords by hand. If the assistant runs the wizard on your behalf, every answer comes back blank and the
blank values overwrite your good saved settings. The wizard refuses to start that way on purpose. If you would
rather be walked through setup step by step, ask the assistant for the manual setup steps and it will guide
you while you type the values yourself.

## What can the setup wizard not do for me?

There are two things the onboarding wizard cannot set up for you.

The first is Jira access. Jira is reached through a connector that you must turn on yourself. Go to claude.ai,
then Settings, then Connectors, and enable Atlassian Rovo. Until you do that, none of the Jira features in
qa-ai will work.

The second is the VPN. The Back Office application that you test against is on the SIT test environment and is
only reachable through the company VPN. Connect the VPN before you ask qa-ai to do anything that opens the
Back Office, otherwise the page simply will not load.

## Where are the full manual setup steps written down?

The complete manual version of every setup step is in the file `SETUP.md` in the qa-ai project folder. The
onboarding wizard automates exactly those steps, so you only need `SETUP.md` if you want to do the setup by
hand or check what the wizard did.

## How do I ask qa-ai to do something?

There are two ways to ask qa-ai for something, and both work equally well. You can write plain English, such
as "generate TCs for AO-306". Or you can use a short command, such as `/review-tcs AO-306`. Use whichever you
find easier to remember.

Always include the Jira ticket number in your request. That single number tells qa-ai which folder to use,
which Google Sheet tab to write to, and which Jira item to link the results to.

If you are not sure what to say, just describe what you want in your own words. qa-ai picks the right tool from
your description. The exact commands exist only for when you want to be quick.

## Why does qa-ai stop and ask me things?

qa-ai pauses and waits for you at a few specific points. This is deliberate. Those are the moments where a
wrong guess would cost you real rework later, so qa-ai checks with you instead of guessing.

qa-ai stops when it is about to save or change a file, so you can read what it is proposing first. qa-ai stops
when it is showing you a plan, so you can confirm the plan or correct the part that is wrong. And qa-ai stops
when it is missing a value it needs, such as a link, a ticket number, or an expected result.

To let qa-ai continue, reply "yes" or "ok". Staying quiet is not a yes, and asking a follow-up question is not
a yes either. qa-ai waits for an actual confirmation.

## How do I stop qa-ai from asking me to confirm everything?

If you are in a hurry and happy to skip the confirmation checks, say "auto mode". qa-ai then stops asking for
confirmation for the rest of the session and saves changes directly. To turn the confirmation checks back on,
say "stop auto mode". If you notice qa-ai saving something without asking you first, auto mode is probably
still on from earlier in the session.

## How do I make test cases for a ticket?

To make test cases for a Jira ticket, say "generate TCs for AO-306", replacing AO-306 with your ticket number.
qa-ai reads the ticket, works out everything that needs testing, writes the test cases, checks its own work,
and then puts the finished cases in the Google Sheet or in Testmo.

The job runs in six stages. First, qa-ai reads the Jira ticket, the design in Figma, and any test cases that
already exist for that ticket. Second, qa-ai shows you what it plans to cover and asks you where the finished
cases should go; this is a stop point where qa-ai waits for your answer. Third, qa-ai writes a coverage plan
and then challenges its own plan looking for holes; this is another stop point. Fourth, qa-ai writes the actual
test cases. Fifth, qa-ai reviews the test cases it just wrote, fixes what it finds, and shows you the totals;
this is the last stop point. Sixth, qa-ai sends the finished cases to the Google Sheet or to Testmo, whichever
you chose earlier.

When the job finishes, you get the test cases in the file `tasks/AO-306/manual-tcs.md`, and the same test cases
in your Google Sheet tab or in Testmo.

## What is the Module question when generating test cases, and why does it matter?

While generating test cases, qa-ai asks you to confirm the Module for the ticket. The Module is the feature
area the test cases belong to. This is the single most important question in the whole job, because the Module
you confirm decides how every test case is named. If you pick the wrong Module, every test case gets the wrong
name and fixing it later means renaming all of them. If you are not sure which Module is correct, ask a
teammate before you confirm.

## How do I report a bug I found?

To report a bug, say `/bug` in the chat. qa-ai works out whether the problem is in the front end or the back
end, captures a screenshot or video as proof, and creates the bug in Jira under the right parent ticket.

The job runs in five stages. First, qa-ai asks you what is wrong and what should have happened instead.
Second, qa-ai shows you the bug it is about to file and checks that nobody has already filed the same bug; this
is a stop point where qa-ai waits for your confirmation. Third, qa-ai reproduces the problem in a browser and
watches what the server sends back. Fourth, qa-ai tells you whether the problem is front end or back end and
explains why; this is another stop point. Fifth, qa-ai captures the evidence and creates the bug in Jira with
the proof attached.

When the job finishes, you get a bug in Jira, filed as a subtask under the parent ticket, with evidence
attached. Copies of the evidence files are saved in the folder `evidence/AO-306/`.

## What do I need before I can report a bug?

You need the parent ticket number. In qa-ai, a bug is always filed as a subtask underneath a parent ticket and
never as a standalone item, so qa-ai cannot start the job without knowing the parent. You also need to be able
to reproduce the problem, because qa-ai never creates a bug without evidence.

## How do I check whether a fix worked?

To check whether a fix worked, say "verify AO-412", replacing AO-412 with the bug's ticket number. qa-ai walks
through the original steps to reproduce on the fixed version, captures fresh evidence, posts the result as a
comment on the ticket, and moves the ticket to the right status.

The job runs in five stages. First, qa-ai reads the bug and its steps to reproduce. Second, qa-ai shows you
what it will test and what counts as a pass or a fail; this is a stop point where qa-ai waits for you. Third,
qa-ai runs the steps and captures evidence, matching the type and number of files the original bug had. Fourth,
qa-ai posts exactly one comment on the ticket, either "Verified FIXED" or "Verified NOT FIXED". Fifth, qa-ai
moves the ticket to the right status.

When the job finishes, you get one comment on the Jira ticket with the evidence attached, and the ticket's
status updated.

## How do I save and share my work with my team?

Your test cases and evidence start out only in the qa-ai project folder on your laptop. To put them somewhere
your team can see them, run three commands in order.

Say `/branch AO-306` to create a separate workspace for that ticket, so your work cannot disturb anyone else's.
Then say `/push` to save and upload your files; qa-ai shows you the list of changed files first and asks which
ones you want to include. Then say `/pr` to open the review request for your team, and qa-ai gives you the
link.

There are two shortcuts. If you say "start task AO-306", qa-ai creates the branch for you automatically. If you
say "done" or "ready to review", qa-ai offers to push your files and open the review request in sequence.

## What do I do the first time I use the git commands on a new laptop?

The first time you use `/branch`, `/push` or `/pr` on a new laptop, say "setup git". qa-ai installs the GitHub
command line tool, asks you for a GitHub personal access token, and connects everything up. You only need to do
this once per laptop. After that, the three git commands work without any further setup.

## How do I get the full content of a Jira ticket in one file?

Say "fetch ticket AO-306 and save". qa-ai retrieves the ticket's description, acceptance criteria, sub-tasks,
comments, linked issues and image attachments, and saves them all into one file you can read offline. Without
the word "save", qa-ai shows you the ticket content in the chat instead of writing a file.

## How do I get the Figma design for a ticket?

Say "get the Figma for AO-306". qa-ai reads the Figma design linked from the ticket and produces a written
description of the design along with screenshots of each screen. This gives you a frozen snapshot of the
design, so your test cases stay stable even if someone edits the Figma file afterwards.

## How do I find test cases that already exist for a ticket?

Say "collect TCs for AO-306". qa-ai finds every test case already stored in Testmo for that ticket and shows
them to you grouped by folder. This is useful before you design anything new, so you do not duplicate work
that already exists.

If the test cases you want are in a Google Sheet rather than in Testmo, say "collect TCs from sheet for AO-306"
instead, and give qa-ai the spreadsheet link when it asks.

## How do I get a second opinion on test cases I already wrote?

Say `/review-tcs AO-306`. qa-ai grades the existing test cases on four things: whether they cover everything
they should, whether each test would actually catch a bug, whether someone else could follow the steps, and
whether they follow the team's format. qa-ai reports what is missing or weak, then applies the fixes once you
approve them.

## How do I check my test plan before I write the test cases?

Say "grill the plan for AO-306". qa-ai challenges every planned test on three points. It asks where the
expected result comes from, because an expected result must trace back to the ticket, an error message, the
live application, or a domain document rather than to guesswork. It asks what the failure path is, because
every scenario should have a negative case or a stated reason why it does not need one. And it asks whether the
test could pass even when the feature is broken, because a test that cannot fail is not worth running. Any
planned test with a gap is flagged for you to resolve.

## How do I push test cases into Testmo?

Say `/to-testmo AO-306`. qa-ai takes the test cases you already have in the ticket's folder and creates each
one in Testmo exactly once, in the right folder, linked to the Jira ticket, with the configurations set and the
state set to Pending Review.

## How do I apply reviewer comments left on the Google Sheet?

Say `/apply-feedback`. qa-ai reads the open comments on the Google Sheet tab, decides what each comment
requires, proposes the change to you, and then applies the smallest edit that satisfies the comment. qa-ai does
not rewrite the whole sheet, so other people's formatting and notes are preserved. If your reviewer left the
feedback on the Jira ticket instead of the Sheet, use `/apply-jira-feedback` instead.

## How do I apply reviewer feedback left on the Jira ticket?

Say `/apply-jira-feedback AO-306`, using the parent ticket number. qa-ai finds the QA Preparation sub-task
underneath that ticket, reads the reviewer's feedback from it, and applies the resulting changes to the test
cases in Testmo.

qa-ai only reads from Jira in this job. Nothing is posted back to the ticket, so the reviewer's thread stays
exactly as they left it.

The job runs in six stages. First, qa-ai locates the QA Preparation sub-task under your ticket. Second, qa-ai
reads and numbers every actionable comment. Third, qa-ai loads the ticket's current test cases from Testmo.
Fourth, qa-ai shows you a table of each comment, the case it affects, the action it requires and the change it
proposes; this is a stop point where you can approve the table, adjust it, or drop individual rows. Fifth,
qa-ai applies the approved changes in Testmo. Sixth, qa-ai reports what actually changed.

If the ticket has no QA Preparation sub-task, qa-ai stops and asks you where the feedback lives rather than
guessing. If there is more than one QA Preparation sub-task, qa-ai lists them and asks which one you mean.

## Does applying feedback ever delete a test case permanently?

No, not by default. When reviewer feedback says a test case should go, qa-ai marks that case as **Deprecated**
in Testmo rather than erasing it. This is deliberate: a Testmo case has no local copy to restore from, so a
permanent delete cannot be undone. If you genuinely want a case erased rather than deprecated, qa-ai asks you
to confirm that specific case by its id before doing it.

## What are the five things qa-ai can do with a reviewer comment?

qa-ai sorts every reviewer comment into one of five actions, and the same five apply whether the feedback came
from a Google Sheet or from a Jira sub-task.

**Delete** means the test case or its content should go entirely. Comments like "remove this", "covered by
TC-12" or "same as the case above" classify as delete.

**Update** means the test case stays but its content changes. Comments correcting an expected result, a
pre-requisite, a module, the steps, the name or the scenario classify as update.

**Add** means a new test case has to exist. Comments like "need to add", "this is missing" or "add a case for
X" classify as add, and qa-ai calls these out as coverage gaps rather than folding them in quietly.

**Defer** means the comment points at a different ticket, so qa-ai records it and changes nothing.

**Ask** means the fix cannot be worked out without a human. qa-ai carries the comment forward to you as the
open question it is, and leaves it for the reviewer to close.

One comment thread normally produces one action. A thread containing two separate requests produces two.

## How do I create a test evidence document for a ticket?

Say `/evidence-doc AO-306`. qa-ai creates a Google Doc containing one heading per test case linked to that
ticket, with blank space underneath each heading for you to paste your screenshots into. It is the empty
container you fill in as you run the tests.

qa-ai first shows you how many cases it found, how they group into folders, and the platform tag it proposes
for the document title; it waits for you to confirm before creating anything. The finished document is titled
in the form `[AO-306] Personal Onboarding (Android app; iOS app)`. If you give qa-ai a Drive folder link, it
puts the document in that folder and tells you where it landed.

## How do I put screenshots into a Google Doc?

Say `/docs-media` and give qa-ai the Google Doc link along with the paths to your local screenshot files. qa-ai
reads the document's structure, works out which image belongs at which point, inserts each one, and then
deletes the temporary upload copies it made along the way. Images are inserted at 450 points wide by default,
which fits an A4 page with margins. If it cannot tell which image belongs where, qa-ai asks you before
inserting anything.

One thing to know: if the document also needs new headings or structure added, qa-ai adds those **before**
inserting any images. Reformatting a Google Doc wipes out images already placed in it, so the order matters.

## How do I build a complete evidence document with screenshots in it?

Building a full evidence document takes three steps, in this order.

First, say `/evidence-doc AO-306` to create the empty document with one heading per test case. Second, capture
your screenshots — either by hand as you test, or by asking qa-ai to capture them while it reproduces
something. Third, say `/docs-media`, give qa-ai the document link and your screenshot paths, and it places each
image under the right heading.

The three steps are separate on purpose, because the middle one is usually you doing the testing.

## How do I explore the application and record how it behaves?

Say "explore this page" or "map this feature". qa-ai drives the live application and records where each value
appears, what the validation rules are, which roles can do what, and which statuses follow which. The result is
a map you and your teammates can rely on when writing test cases, instead of everyone rediscovering the same
behaviour.

## How do I hand my work over to someone else?

Say `/handoff`. qa-ai writes a document that another person, or another assistant session, can pick the work up
from. The document covers the goal, what is done and what is left, the decisions made and why, what was learned
along the way, and what was tried and failed. It is a state transfer document, not a summary of the
conversation.

## How do I get my plan or design challenged before I commit to it?

Say `/grill-me`. qa-ai runs a relentless interview against whatever plan or design you bring it, pushing on the
parts you have not thought through. Use it when you want your own thinking stress-tested rather than agreed
with.

This one only runs when you ask for it by name. qa-ai will never start a grilling on its own, however shaky the
plan looks.

## What is the difference between /grill-me and grilling a test plan?

They sound alike but they do different jobs. `/grill-me` interviews **you** about any plan or design you are
working on, and you have to type it to start it. Saying "grill the plan for AO-306" instead challenges the
**test coverage plan** for a specific ticket, checking each planned test for its expected-result source, its
failure path, and whether it could pass on a broken build.

Use `/grill-me` when you are thinking something through. Use "grill the plan for AO-306" when you are about to
write test cases.

## How do I get shorter replies from qa-ai?

Say `/caveman` or "be brief". qa-ai then gives much shorter answers for the rest of the session, keeping all the
technical substance and dropping the padding. To go back to normal length replies, say "normal mode" or "stop
caveman".

## Where does qa-ai save my files?

Everything for one ticket lives in a single folder named after the ticket. For ticket AO-306, the folder is
`tasks/AO-306/`.

Inside that folder, the file `jira.md` holds the ticket saved so you can read it offline. The file `tc.md` holds
test cases that already existed for the ticket. The file `tc-plan.md` holds the plan of what is going to be
tested. The file `manual-tcs.md` holds the finished test cases, and this is the file you will usually want to
open. The file `tc-review.md` holds what the review found. The folder `attachments/` holds images from the
ticket and from the Figma design.

Outside the ticket folder, `evidence/AO-306/` holds screenshots and videos captured for bug reports, and
`reports/AO-306/` holds coverage reports.

## Which file should I open to read the finished test cases?

Open `tasks/AO-306/manual-tcs.md`, replacing AO-306 with your ticket number. When qa-ai says "Written to
tasks/AO-306/manual-tcs.md", that file is the actual work. The chat only shows you a summary and anything qa-ai
needs you to decide, so the file is where you should review the detail.

## Why will the Back Office page not load?

The Back Office application you test against is on the SIT test environment and is only reachable through the
company VPN. Connect the VPN and try again. This is the most common reason a page fails to load when using
qa-ai.

## Why do the Jira features not work at all?

Jira access in qa-ai comes through a connector you must enable yourself. Go to claude.ai, then Settings, then
Connectors, and turn on Atlassian Rovo. This cannot be set up by the onboarding wizard or from the Terminal. If
no Jira features work at all, this is almost always the reason.

## Why does Testmo, Figma or Google Sheets fail?

If Testmo, Figma or Google Sheets fails, that connection is not set up on your laptop. Run `./onboarding.sh`
again in the qa-ai project folder. The wizard detects what is already working and only fills in the missing
pieces, so re-running it is safe.

## Why does qa-ai keep asking me for a value I expected it to know?

qa-ai is designed to ask rather than guess, so being asked once is normal — just give it the value. If qa-ai
keeps asking for the same value every time, that setting is missing from your configuration. Re-run
`./onboarding.sh` to fill it in, or ask a teammate which value belongs there.

## What does "You are on a protected branch" mean?

That message means you tried to save or upload files while working directly on the team's main copy. qa-ai
blocks this to stop you writing over everyone else's work. Say `/branch AO-306` first to create your own
workspace for the ticket, then try your command again. This block has no override, because working directly on
the main copy is never the right thing to do.

## What if /pr says gh is missing or logged out?

That means the GitHub command line tool is not installed on your laptop, or your access token has expired. Say
"setup git" and qa-ai fixes both, including replacing an expired token. Then run `/pr` again.

## What happens if I stop qa-ai halfway through a job?

Nothing is lost. Every job checks what already exists in the ticket's folder and restarts at the first step
whose result is missing. Say the same thing again later and qa-ai continues from where it stopped rather than
redoing the work. Anything already produced is shown to you again for confirmation, never silently overwritten.

## What do the abbreviations in qa-ai mean?

A **ticket** is a Jira item, such as AO-306. The ticket number is what you will type most often when using
qa-ai.

A **test case**, often shortened to **TC**, is one written test: the steps to follow and what should happen.

**AC** stands for acceptance criteria, which is what the ticket promises the feature will do.

**Testmo** is the tool where the team keeps its test cases.

**SIT** is the test environment, meaning the copy of the application you test against rather than the real
one used by customers.

**STR** stands for steps to reproduce, which is how to make a bug happen again.

**Evidence** is the screenshot or video that proves a bug is real. qa-ai never files a bug without evidence.

A **Module** is the feature area a test case belongs to. The Module decides how test cases are named.

## Who maintains qa-ai and where are its rules kept?

The QA team maintains qa-ai. Its rules live in the folder `.claude/steering/` in the project, covering the test
case format, the bug format, priority scoring, the reviewer-feedback actions, the Jira and Testmo identifiers,
and the browser rules. Changing
a rule there changes every job that uses it. What the application under test actually does is recorded
separately in `.claude/domain/`.

If you maintain qa-ai, note two standing rules. Never hand-edit anything in the `.kiro/` folder, because it is
generated automatically from `.claude/` by running `python3 sync-kiro.py`. And never stage every file at once
with a blanket git add, because every ticket's working files are tracked and a blanket add would sweep in other
people's work.

## Where can I find more detail than this document?

This document covers what you need in order to use qa-ai. There is a fuller technical description of the whole
framework in `README.md`. The definitive description of each individual job is the skill file itself, under
`.claude/skills/`. If this document and a skill file ever disagree, the skill file is correct.
