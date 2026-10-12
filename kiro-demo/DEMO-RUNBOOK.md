# Kiro demo runbook (Future Builders Connect, Coimbatore)

There are two prepared folders in this kit:

| Folder | Used in | Live or prepared |
| --- | --- | --- |
| `demo-api/` | Section 8: live demo (rate limiting on an existing API) | **Live** on stage |
| `loomtrack/` | Section 9: Scenario 1 (LoomTrack) | **Prepared tonight**, shown on stage |

Scenario 2 (first week on a team) is told as a story. It needs no demo.

Menu and button names in Kiro change between versions. If a label below doesn't match your screen, look for the closest equivalent.

---

## Part A: Tonight (about 60–90 minutes)

### 1. Install and sign in (10 min)
1. Download Kiro IDE from https://kiro.dev/downloads and install it.
2. Open it and sign in with GitHub or Google.
3. In the model picker, choose **Auto** (it's fast and cheap). Check that you have credits left.

### 2. Set up demo-api (10 min)
In a terminal, inside `demo-api/`:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q              # expect: 5 passed
```

Then save a clean starting point so you can reset after rehearsing:

```bash
git init
git add -A
git commit -m "Baseline before demo"
```

### 3. Open it in Kiro and check steering (5 min)
1. **File > Open Folder** and pick `demo-api/`.
2. Open the Kiro panel (the Kiro icon in the left sidebar). Under **Steering**, you should see `product.md`, `structure.md` and `tech.md`.
3. Ask Kiro in chat: *"What is this project and what are its conventions?"* It should mention FastAPI, data isolation and the rule about putting rate limiting in its own module. That shows steering works.

### 4. Create the hook in advance (5 min)
1. In the Kiro panel, find **Agent Hooks** and add a new hook.
2. Describe it in plain English:
   > When any Python file in app/ or tests/ is saved, run `python -m pytest -q` and tell me if anything fails.
3. Test it: open `app/main.py`, add a blank line, save. The hook should run.
4. Commit it: `git add -A && git commit -m "Add test-on-save hook"`.

This commit is now your **baseline**. You reset to it after the rehearsal.

### 5. Full rehearsal with a screen recording (20–25 min)
Start a screen recording first. Use OBS, the Windows Game Bar (**Win + G**) or macOS (**Cmd + Shift + 5**). This recording is your backup if the Wi-Fi fails tomorrow.

Then follow **Part C** exactly, as if you were on stage. Time it. Afterwards, save the finished result on its own branch:

```bash
git checkout -b rehearsal-result
git add -A
git commit -m "Rehearsal result: rate limiting done"
git checkout main                 # or master, whichever git created
```

### 6. Prepare LoomTrack (20–30 min)
1. Open the `loomtrack/` folder in Kiro and run `git init && git add -A && git commit -m "Steering only"`.
2. Start a new **Spec** session and paste the prompt from `loomtrack/README.md`.
3. Review the requirements. Check the four rules listed in that README. Note anything Kiro got differently, because you'll say it on stage.
4. Approve the requirements, then the design, then the tasks.
5. Run the tasks (**Run all tasks**, or one by one). Then run `python -m pytest -q`.
6. Write down which property tests it created and whether any failed along the way. That's your real story for the script.
7. Commit everything. Take screenshots of `requirements.md`, `design.md`, `tasks.md` and one property test.

### 7. Before bed
- Reset demo-api: `git checkout main && git reset --hard && git clean -fd`, then run `python -m pytest -q` (5 passed).
- Delete any spec folder left over from the rehearsal on main, if one is there.
- Charge your laptop.

---

## Part B: Morning of the talk (15 min)

- [ ] Laptop charged. Charger and HDMI / USB-C adapter in your bag.
- [ ] Phone hotspot ready as a backup for the venue Wi-Fi.
- [ ] Do Not Disturb on. Close Slack, mail and WhatsApp desktop.
- [ ] Kiro open with `demo-api/` at the baseline. Run `git status`: it should be clean.
- [ ] Editor zoomed in. Press **Ctrl/Cmd and +** three or four times. Terminal font large.
- [ ] Two terminals open in `demo-api/` with the venv active: one for the server, one for commands.
- [ ] Rehearsal recording open in a video player, minimised.
- [ ] LoomTrack folder open in a second Kiro window, with screenshots ready.
- [ ] Credits checked and the model set to Auto.

---

## Part C: The live demo on stage (8 minutes)

### Step 1: Show the project and its steering (1 min)
- Show `app/main.py` briefly: "a small API where clients export their orders as CSV."
- Open the Kiro panel and show the three steering files.
- Terminal 1: `uvicorn app.main:app`
- Terminal 2: `./hit-export.sh` (Windows: `.\hit-export.ps1`). All six requests return **200**. Say: *"Right now, anyone can hammer this expensive endpoint."*

### Step 2: The prompt (1 min)
Start a new **Spec** session and type or paste:

> Add rate limiting to the /reports/export endpoint. Each API key may call it at most 5 times per minute. When the limit is exceeded, return HTTP 429 with a Retry-After header and a JSON detail message. Other endpoints must not be limited. Write property-based tests with Hypothesis.

### Step 3: Review the spec (3 min)
- Open `requirements.md` and read one WHEN / THEN acceptance criterion aloud.
- **Edit it live:** change *5 times per minute* to **3 times per minute**. Say: *"I'm in control of the intent."*
- Ask Kiro in chat: *"I changed the limit to 3 per minute. Please update the design and tasks to match."*
- Open `design.md` and point out that it created a separate module plugged in with `Depends`. *"That's my structure.md steering at work."*
- Open `tasks.md`.

### Step 4: Build it (3 min)
- Start the first task or two. Talk while it works: *"Notice it's using my stack and my conventions."*
- When it's done, open the property test. Point out that it states a rule ("for any sequence of requests, at most N succeed per window") and refers back to a requirement.
- Terminal 2: `python -m pytest -q`

### Step 5: Prove it and show the hook (1 min)
- Restart the server in terminal 1 (Ctrl+C, then `uvicorn app.main:app`).
- Terminal 2: `./hit-export.sh`. Now you see **200, 200, 200, 429, 429, 429**. That's the payoff moment, so pause and let the room see it.
- Save any file and let the hook run the tests.

---

## Part D: If something goes wrong

| Problem | What to say | What to do |
| --- | --- | --- |
| Generation is slow | "While the agent thinks, let me show you what this looked like last night." | `git stash -u && git checkout rehearsal-result`, then show the files. |
| Wi-Fi or login fails | "The conference Wi-Fi has opinions today. Luckily, I recorded this." | Switch to the phone hotspot, or play the recording and narrate over it. |
| Tests fail | "This is exactly why we test. Let's ask Kiro." | Paste the failure into chat once. If it's not fixed in 30 seconds, switch to `rehearsal-result`. |
| Running out of time | "I'll skip ahead to the result." | Skip to Step 5 using `rehearsal-result`. |

Never debug live for more than 30 seconds.

## Reset after the talk (or between rehearsals)

```bash
git checkout main && git reset --hard && git clean -fd
```
