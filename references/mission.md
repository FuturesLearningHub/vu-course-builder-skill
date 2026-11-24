# The Chancellor's charge (`#mission`)

Every course carries this section. It is the institutional why. It comes
third in the spine, after the belief and before How it works. Its pager entry
is:

```js
{ sel:'#mission', key:'mission', label:'The Chancellor’s charge', mode:'whole' }
```

It is always `th-dark`, always one page, and never tracked for progress.

## What you may change

Copy the HTML below exactly. Only the three slots change from course to
course. Everything else stays word for word, including the eyebrow, the
headline, the vision sentence, the three Areas of Focus, the first two
sentences of the flywheel and the source line.

| Slot | Where | What to write | Length |
|---|---|---|---|
| `SLOT 1: dare` | End of the lead paragraph, after "dare to grow, and" | Finish the sentence with this course's dare: what growing looks like at the learner's desk in this subject | One clause, about 10 to 20 words |
| `SLOT 2: delivers` | The "How this course delivers" box | Name the course. Tie it to one or more of the three focus areas by their exact names (Exceptional Core Operations, Bold Strategic Initiatives, Values Leadership) | One or two sentences |
| `SLOT 3: your place` | The flywheel box, after "Here's your place in it:" | Say how this course's skill feeds talent, funding, partnerships, access or reputation. End on what the learner does at their own desk | Two sentences |

Slot rules:

- Use the course's own vocabulary (its framework names, its key move). The
  slot should not fit any other course.
- Use no em or en dashes and no "not X, but Y". Do not invent a new claim
  about the university.
- Do not change the bold phrases, the headline or the quoted focus-area text.
  They are the Chancellor's words.
- Write `&rsquo;` and `&ldquo;`/`&rdquo;` entities as the template does.

## Examples from shipped courses

**SLOT 1: dare**

- Working Smarter: "right now the dare on a staff desk is learning the new
  tools by using them."
- Difficult Conversations: "the conversation you have been putting off is
  exactly that kind of dare."
- Trust, Then Verify: "daring work travels on facts somebody bothered to
  check."
- Numbers Faster: "growth shows up first in the numbers, so somebody has to
  read them faster than by hand."

**SLOT 2: delivers**

- Working Smarter (series default, use it only for a series overview
  course): "Every course in this collection helps you deliver on that
  mission: each one turns an everyday task into Exceptional Core Operations,
  frees fuel for Bold Strategic Initiatives, and models the careful use Values
  Leadership asks for."
- Trust, Then Verify: "Trust, Then Verify is Values Leadership in daily
  practice: AI output checked before it ships lets Vanderbilt move at the
  speed of Exceptional Core Operations without spending the reputation the
  vision depends on."
- Difficult Conversations: "Navigating Difficult Conversations serves the
  mission where it is hardest: problems named early keep core operations
  exceptional, and a culture that talks straight is Values Leadership made
  visible."

**SLOT 3: your place**

- Working Smarter: "execution with ambition is a staff that works faster with
  AI and still checks every name, number, and date before it ships, and
  values-driven leadership looks like sensitive data going only to approved
  tools without anyone having to ask. Every well-routed task and every
  verified answer feeds the wheel from your desk."
- Trust, Then Verify: "reputation is the flywheel's fuel, and an unverified
  number in a public report is exactly what burns it. Verification sized to
  the stakes keeps everything that leaves your desk worthy of the
  university's name."
- Difficult Conversations: "talent stays where trust is real, and trust is
  built or spent in exactly the conversations this course teaches."

## The section (book-mode courses)

This is the Working Smarter markup. Paste it as the third top-level block in
`<main>` and replace the three `[SLOT ...]` markers along with their
comments.

```html
<!-- ═══════════════════ THE CHANCELLOR'S CHARGE ═══════════════════
     The institutional why: Chancellor Diermeier's vision, the three annual
     focus areas, and the reputation flywheel, each tied to this course. -->
<section id="mission" class="th-dark" aria-label="The Chancellor&rsquo;s charge">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow"><span class="tick" aria-hidden="true"></span><span class="mono">The institutional why &middot; Crescere aude</span></span>
      <h2>Vanderbilt will define the great university of the 21st Century and <em>be it.</em></h2>
      <p>That is Chancellor Diermeier&rsquo;s institutional vision, one sentence with no hedge in it. The how is equally blunt: operate at <b>uncommon speed, agility, and scale</b> to address society&rsquo;s challenges through education and research, and help <b>reclaim the essential role of leading research universities in driving American prosperity</b>. Our motto has always been the dare, <em>Crescere aude</em>, dare to grow, and [SLOT 1: dare].</p>
    </div>
    <span class="eyebrow" style="margin-bottom:10px"><span class="tick" aria-hidden="true"></span><span class="mono">Areas of Focus</span></span>
    <h3 style="font-size:1.35rem;margin:10px 0 18px">Three ways Vanderbilt delivers on the vision</h3>
    <div class="resp-grid">
      <article class="principle reveal">
        <span class="mono" style="display:block;font-size:.72rem;letter-spacing:.07em;margin-bottom:12px">1</span>
        <h3>Exceptional Core Operations</h3>
        <p>With speed, agility and scale, Vanderbilt will distinguish itself with innovative and impactful capabilities to ensure that we have the talent, resources and reputation necessary to deliver on our vision.</p>
      </article>
      <article class="principle reveal" style="transition-delay:.06s">
        <span class="mono" style="display:block;font-size:.72rem;letter-spacing:.07em;margin-bottom:12px">2</span>
        <h3>Bold Strategic Initiatives</h3>
        <p>With “exceptional core operations” as our fuel, Vanderbilt will pursue increasingly bold initiatives that enable and enhance the reach and impact of our education and research mission.</p>
      </article>
      <article class="principle reveal" style="transition-delay:.12s">
        <span class="mono" style="display:block;font-size:.72rem;letter-spacing:.07em;margin-bottom:12px">3</span>
        <h3>Values Leadership</h3>
        <p>Through strategic advocacy efforts and modeling the role of an essential research university, Vanderbilt will stimulate industry change and combat existential threats to our education and research mission.</p>
      </article>
    </div>
    <div class="evidence">
      <span class="e-label">How this course delivers</span>
      <p>[SLOT 2: delivers]</p>
    </div>
    <div class="evidence reveal">
      <span class="e-label">The reputation flywheel</span>
      <p>Reputation and resources feed each other in a loop, reputation attracts <b>talent, funding, partnerships, and access</b>, which build the reputation. The university spins that flywheel with <b>execution with ambition, values-driven leadership, and athletics momentum</b>. Here&rsquo;s your place in it: [SLOT 3: your place]</p>
      <span class="e-src">&ldquo;Daring to Grow&rdquo;, Chancellor Diermeier, Vanderbilt University (July 2022): <a href="https://news.vanderbilt.edu/2022/07/01/daring-to-grow-together-we-are-building-the-great-university-of-the-21st-century/" target="_blank" rel="noopener">the vision statement this page draws from</a></span>
    </div>
  </div>
</section>
```

## Legacy deck courses

The older horizontal-deck courses carry the same text in a slide:
`<section class="slide on-dark" id="s-mission" data-title="The Chancellor's charge">`.
It uses `p.eyebrow`, `p.lead`, `span.tag` labels and a "Source:" line. Keep
the words identical to the block above and the markup in that repo's own
style (see `deck.md`). The facilitator screenshot for this page is
`facilitator/img/s-mission.jpg` (deck) or `facilitator/img/mission.jpg`
(book mode).

## Checks before publish

- `grep -c 'id="mission"'` returns 1 in each edition.
- `grep '\[SLOT'` returns nothing.
- Diff the section against the block above. Only the three slots may differ.
- The `mission` entry is in `PLAN` and is not in `TRACKED`.
- If the audit script's section list is hard-coded, `mission` is in it. The
  bundled `a11y-audit.mjs` finds pages on its own.
