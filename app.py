"""
Election Process Assistant — Interactive AI-Powered Guide
Built with Flask · Python-only stack
"""

from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# ─────────────────────────────────────────────
# DATA: Timeline stages
# ─────────────────────────────────────────────
TIMELINE_STAGES = [
    {
        "id": 1,
        "title": "Candidate Declaration",
        "icon": "🎤",
        "date_range": "12–18 months before election",
        "summary": "Candidates formally announce their intention to run for office, forming exploratory committees and beginning to build campaign infrastructure.",
        "details": [
            "File official candidacy paperwork with election authorities",
            "Form an exploratory committee to gauge support and raise initial funds",
            "Announce candidacy publicly, often at a major rally or media event",
            "Begin assembling a campaign team: manager, communications director, finance chair",
            "Start building a donor base and establishing campaign accounts",
        ],
        "deep_dive": "Explain the full process of declaring candidacy for a major election, including legal requirements, FEC filings, and strategic considerations for timing the announcement.",
    },
    {
        "id": 2,
        "title": "Primary Campaigns",
        "icon": "📢",
        "date_range": "6–12 months before election",
        "summary": "Candidates campaign within their party to win the nomination, debating rivals and courting voters in early-voting states.",
        "details": [
            "Participate in party debates to differentiate from rivals",
            "Campaign in early primary/caucus states like Iowa and New Hampshire",
            "Build grassroots organizations and volunteer networks",
            "Run advertising campaigns across TV, digital, and social media",
            "Secure endorsements from party leaders and influential figures",
        ],
        "deep_dive": "Describe how primary campaigns work, the difference between primaries and caucuses, the role of superdelegates, and why early states matter so much.",
    },
    {
        "id": 3,
        "title": "Primaries & Caucuses",
        "icon": "🗳️",
        "date_range": "January – June of election year",
        "summary": "Voters in each state cast ballots or attend caucuses to select delegates who will support their preferred candidate at the national convention.",
        "details": [
            "Open primaries allow any registered voter; closed primaries restrict to party members",
            "Caucuses are local gatherings where voters publicly debate and align with candidates",
            "Delegates are awarded proportionally or winner-take-all depending on state and party rules",
            "Super Tuesday sees multiple states voting simultaneously, often deciding the frontrunner",
            "Candidates who underperform may suspend their campaigns and endorse rivals",
        ],
        "deep_dive": "Give a deep explanation of primaries vs caucuses, how delegates are allocated, the significance of Super Tuesday, and historical examples of contested primaries.",
    },
    {
        "id": 4,
        "title": "National Conventions",
        "icon": "🏛️",
        "date_range": "July – August of election year",
        "summary": "Each party holds a multi-day convention to formally nominate their presidential candidate and adopt a party platform.",
        "details": [
            "Delegates cast official votes to nominate the party's candidate",
            "The nominee selects and announces their vice-presidential running mate",
            "The party adopts its official platform outlining policy positions",
            "Major speeches by party leaders, the nominee, and rising stars energize the base",
            "Conventions typically generate a 'bounce' in opinion polls for the nominee",
        ],
        "deep_dive": "Explain how national conventions work, the history of brokered conventions, how VP picks are chosen, and the role of party platforms in American politics.",
    },
    {
        "id": 5,
        "title": "General Election Campaign",
        "icon": "⚔️",
        "date_range": "August – November of election year",
        "summary": "Nominees from both major parties face off in the general election, debating head-to-head and campaigning across battleground states.",
        "details": [
            "Presidential debates are held, typically three, plus one vice-presidential debate",
            "Campaigns focus resources on swing states that could go either way",
            "Massive advertising blitzes across all media channels",
            "Get-out-the-vote operations mobilize supporters for Election Day",
            "October surprises — unexpected late-breaking events — can shift momentum",
        ],
        "deep_dive": "Describe the general election campaign strategy, the role of swing states, how presidential debates work, and the impact of campaign finance on elections.",
    },
    {
        "id": 6,
        "title": "Election Day",
        "icon": "📊",
        "date_range": "First Tuesday after November 1",
        "summary": "Citizens cast their votes at polling stations or through mail-in/early voting. Results are tallied and projected throughout the evening.",
        "details": [
            "Polls open and close at times set by each state",
            "Early voting and mail-in ballots are counted alongside Election Day votes",
            "Exit polls provide early indications of voter preferences and demographics",
            "Media networks project winners based on vote counts and statistical models",
            "Close races may not be called for days as all ballots are counted",
        ],
        "deep_dive": "Explain how Election Day works in detail: poll operations, vote counting procedures, the role of exit polls, how media projects winners, and what happens with contested results.",
    },
    {
        "id": 7,
        "title": "Electoral College Vote",
        "icon": "⚖️",
        "date_range": "First Monday after the second Wednesday in December",
        "summary": "Electors in each state formally cast their votes for president and vice president based on the popular vote results in their state.",
        "details": [
            "Each state gets electors equal to its total Congressional representation",
            "Most states use winner-take-all: the popular vote winner gets all electoral votes",
            "270 electoral votes out of 538 are needed to win the presidency",
            "Faithless electors occasionally vote against their state's popular vote winner",
            "Congress certifies the electoral vote results in a joint session in January",
        ],
        "deep_dive": "Give a comprehensive explanation of the Electoral College: its history, how electors are chosen, the winner-take-all system, faithless electors, and the ongoing debate about abolishing it.",
    },
    {
        "id": 8,
        "title": "Inauguration",
        "icon": "🇺🇸",
        "date_range": "January 20 following the election",
        "summary": "The president-elect is sworn into office on the steps of the U.S. Capitol, delivering an inaugural address outlining their vision for the country.",
        "details": [
            "The Chief Justice of the Supreme Court administers the oath of office",
            "The new president delivers an inaugural address to the nation",
            "A transition of power occurs as the outgoing president departs the White House",
            "Inaugural balls and celebrations mark the occasion in Washington, D.C.",
            "The new administration begins executing its policy agenda immediately",
        ],
        "deep_dive": "Describe the inauguration ceremony in detail, its history and traditions, famous inaugural addresses, the peaceful transfer of power, and what happens during the transition period.",
    },
]

# ─────────────────────────────────────────────
# DATA: Quiz questions
# ─────────────────────────────────────────────
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "In a First-Past-the-Post (FPTP) system, how is the winner determined?",
        "options": [
            "The candidate with more than 50% of votes",
            "The candidate with the most votes, regardless of majority",
            "Through a runoff between the top two candidates",
            "By proportional allocation of seats",
        ],
        "correct": 1,
        "explanation": "In FPTP (also called 'plurality voting'), the candidate who receives the most votes wins — even if they don't achieve an absolute majority (50%+1). This is used in the US, UK, Canada, and India.",
    },
    {
        "id": 2,
        "question": "What is gerrymandering?",
        "options": [
            "The process of registering new voters before an election",
            "Manipulating electoral district boundaries to favor a party",
            "The practice of voting in multiple districts",
            "A method of counting absentee ballots",
        ],
        "correct": 1,
        "explanation": "Gerrymandering is the deliberate manipulation of electoral district boundaries to create unfair advantages for a particular political party. The term dates to 1812, named after Governor Elbridge Gerry of Massachusetts.",
    },
    {
        "id": 3,
        "question": "In a proportional representation system, how are seats allocated?",
        "options": [
            "Winner takes all seats in each district",
            "Seats are given to the largest party only",
            "Seats are distributed in proportion to vote share",
            "Seats are allocated by a judicial panel",
        ],
        "correct": 2,
        "explanation": "Proportional representation allocates parliamentary seats to parties based on the percentage of votes they receive. If a party gets 30% of votes, they get approximately 30% of seats. Used in Germany, Netherlands, and many other nations.",
    },
    {
        "id": 4,
        "question": "What happens in a 'hung parliament'?",
        "options": [
            "The ruling party is automatically re-elected",
            "New elections must be held immediately",
            "No single party wins an outright majority of seats",
            "The parliament is dissolved permanently",
        ],
        "correct": 2,
        "explanation": "A hung parliament occurs when no single party wins enough seats for an outright majority. This typically leads to coalition negotiations, minority government formation, or in some cases, fresh elections.",
    },
    {
        "id": 5,
        "question": "How many electoral votes are needed to win the U.S. presidency?",
        "options": [
            "200",
            "270",
            "300",
            "538",
        ],
        "correct": 1,
        "explanation": "A candidate needs 270 out of 538 total electoral votes to win the U.S. presidency. The total of 538 comes from 435 House members + 100 Senators + 3 electors from Washington, D.C.",
    },
]

# ─────────────────────────────────────────────
# DATA: Glossary
# ─────────────────────────────────────────────
GLOSSARY_TERMS = [
    {"term": "Ballot", "definition": "The physical or electronic form used by voters to cast their vote in an election. Can be paper, mechanical, or digital."},
    {"term": "Caucus", "definition": "A local gathering of party members who publicly discuss and vote for their preferred candidate, used in some U.S. states instead of primaries."},
    {"term": "Constituency", "definition": "A geographic area whose voters elect a representative. Also called a district, riding, or electorate in different countries."},
    {"term": "Delegate", "definition": "A person chosen to represent a state or district at a party's national convention, pledged to vote for a specific candidate."},
    {"term": "Electoral College", "definition": "The body of 538 electors who formally elect the U.S. President and Vice President based on each state's popular vote results."},
    {"term": "Franchise", "definition": "The legal right to vote in public elections. Also known as suffrage. Has been expanded over centuries to include women and minorities."},
    {"term": "Gerrymandering", "definition": "The practice of drawing electoral district boundaries to give one political party an unfair advantage over its rivals."},
    {"term": "Hung Parliament", "definition": "A situation where no single political party wins an absolute majority of seats, requiring coalition formation or minority governance."},
    {"term": "Incumbent", "definition": "The current holder of a political office who may be seeking re-election. Incumbents often have advantages in name recognition and fundraising."},
    {"term": "Mandate", "definition": "The authority granted by voters to a winning candidate or party to implement the policies they campaigned on."},
    {"term": "Plurality", "definition": "The largest number of votes received by any candidate in an election, even if it's not a majority (more than 50%)."},
    {"term": "Proportional Representation", "definition": "An electoral system where seats in a legislature are allocated to parties in proportion to the number of votes each receives."},
    {"term": "Referendum", "definition": "A direct vote by the electorate on a specific political question or policy, such as constitutional amendments or EU membership."},
    {"term": "Swing State", "definition": "A state where neither major party has a strong majority, making it competitive and crucial in determining election outcomes."},
    {"term": "Turnout", "definition": "The percentage of eligible voters who actually cast a ballot in an election. Higher turnout is generally seen as a sign of democratic health."},
]

# ─────────────────────────────────────────────
# DATA: World comparison
# ─────────────────────────────────────────────
WORLD_COMPARE = [
    {
        "country": "United States",
        "flag": "🇺🇸",
        "system": "Presidential Republic",
        "electoral_system": "First-Past-the-Post with Electoral College",
        "voting_method": "Paper & electronic ballots; in-person, mail-in, early voting",
        "term_length": "4 years (max 2 terms)",
        "turnout": "~66% (2020)",
        "fun_fact": "The U.S. is one of the few democracies that doesn't have automatic voter registration.",
        "deep_dive": "Give a comprehensive overview of the U.S. electoral system, including the Electoral College, the primary system, campaign finance, the role of swing states, and current reform debates.",
    },
    {
        "country": "United Kingdom",
        "flag": "🇬🇧",
        "system": "Parliamentary Constitutional Monarchy",
        "electoral_system": "First-Past-the-Post (Westminster system)",
        "voting_method": "Paper ballots marked with X; in-person and postal voting",
        "term_length": "5 years (PM, no term limits)",
        "turnout": "~67% (2019)",
        "fun_fact": "The UK has no codified constitution — it relies on conventions, statutes, and judicial decisions.",
        "deep_dive": "Explain the UK's Westminster parliamentary system, how the Prime Minister is chosen, the role of the monarchy, the House of Lords vs Commons, and debates about proportional representation.",
    },
    {
        "country": "India",
        "flag": "🇮🇳",
        "system": "Parliamentary Federal Republic",
        "electoral_system": "First-Past-the-Post (Lok Sabha)",
        "voting_method": "Electronic Voting Machines (EVMs) with VVPAT",
        "term_length": "5 years (PM, no term limits)",
        "turnout": "~67% (2024)",
        "fun_fact": "India's general elections are the largest democratic exercise in the world, with nearly 970 million eligible voters.",
        "deep_dive": "Describe India's electoral system in detail: the Election Commission, the phased voting process across 28 states, the role of EVMs, coalition politics, and anti-defection laws.",
    },
    {
        "country": "Germany",
        "flag": "🇩🇪",
        "system": "Parliamentary Federal Republic",
        "electoral_system": "Mixed-Member Proportional (MMP)",
        "voting_method": "Paper ballots; two votes (direct candidate + party list)",
        "term_length": "4 years (Chancellor, no term limits)",
        "turnout": "~76% (2021)",
        "fun_fact": "Germany's two-vote system gives citizens both a local representative and proportional party representation.",
        "deep_dive": "Explain Germany's Mixed-Member Proportional system, the two-vote mechanism, the 5% threshold, how coalition governments form, and why it's considered one of the most representative systems.",
    },
]

# ─────────────────────────────────────────────
# DATA: Quick-start prompts
# ─────────────────────────────────────────────
QUICK_PROMPTS = [
    {
        "icon": "🗺️",
        "title": "Gerrymandering Explained",
        "prompt": "Explain gerrymandering in depth: its history, techniques like packing and cracking, famous examples, Supreme Court rulings, and current reform efforts.",
    },
    {
        "icon": "🏛️",
        "title": "Electoral College Deep Dive",
        "prompt": "Give a comprehensive analysis of the Electoral College: how it works, why the founders created it, arguments for and against it, and proposed alternatives.",
    },
    {
        "icon": "📝",
        "title": "Voter Registration Guide",
        "prompt": "Explain the voter registration process across different democracies, automatic vs. opt-in systems, barriers to registration, and how technology is changing the process.",
    },
    {
        "icon": "🔒",
        "title": "Election Security",
        "prompt": "Discuss election security in modern democracies: threats from cyberattacks, disinformation, voting machine vulnerabilities, and what safeguards exist to protect election integrity.",
    },
    {
        "icon": "📊",
        "title": "Polling & Predictions",
        "prompt": "How do election polls work? Explain polling methodologies, margin of error, why polls can be wrong, the role of aggregators, and how exit polls differ from pre-election polls.",
    },
    {
        "icon": "💰",
        "title": "Campaign Finance",
        "prompt": "Explain campaign finance in elections: fundraising methods, PACs and Super PACs, the impact of Citizens United, spending limits, dark money, and reform proposals.",
    },
    {
        "icon": "🌍",
        "title": "Voting Systems Compared",
        "prompt": "Compare the world's major voting systems: FPTP, proportional representation, ranked-choice, two-round systems, and mixed-member proportional. What are the pros and cons of each?",
    },
    {
        "icon": "⚖️",
        "title": "Voter Suppression",
        "prompt": "Discuss voter suppression tactics historically and today: voter ID laws, purging rolls, reducing polling locations, and legal battles over voting rights.",
    },
]


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template(
        "index.html",
        timeline=TIMELINE_STAGES,
        quiz=QUIZ_QUESTIONS,
        glossary=GLOSSARY_TERMS,
        compare=WORLD_COMPARE,
        prompts=QUICK_PROMPTS,
    )


@app.route("/api/quiz", methods=["GET"])
def get_quiz():
    return jsonify(QUIZ_QUESTIONS)


@app.route("/api/quiz/check", methods=["POST"])
def check_answer():
    data = request.get_json()
    question_id = data.get("question_id")
    answer = data.get("answer")
    for q in QUIZ_QUESTIONS:
        if q["id"] == question_id:
            correct = q["correct"] == answer
            return jsonify(
                {
                    "correct": correct,
                    "explanation": q["explanation"],
                    "correct_answer": q["correct"],
                }
            )
    return jsonify({"error": "Question not found"}), 404


@app.route("/api/timeline")
def get_timeline():
    return jsonify(TIMELINE_STAGES)


@app.route("/api/glossary")
def get_glossary():
    return jsonify(GLOSSARY_TERMS)


@app.route("/api/compare")
def get_compare():
    return jsonify(WORLD_COMPARE)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
