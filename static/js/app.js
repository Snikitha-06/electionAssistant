/* ═══════════════════════════════════════════
   Election Process Assistant — App Logic
   ═══════════════════════════════════════════ */

// ── TAB NAVIGATION ──────────────────────────
const tabBtns = document.querySelectorAll('.tabs__btn');
const sections = document.querySelectorAll('.section');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.tab;
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        sections.forEach(s => {
            s.classList.remove('section--active');
            s.style.animation = 'none';
        });
        const sec = document.getElementById('section-' + target);
        if (sec) {
            sec.classList.add('section--active');
            void sec.offsetWidth; // reflow
            sec.style.animation = 'fadeIn 0.4s ease';
        }
        // Init quiz on first visit
        if (target === 'quiz' && !quizInitialized) initQuiz();
    });
});

// ── TIMELINE ────────────────────────────────
function toggleTimeline(id) {
    const item = document.querySelector(`.timeline__item[data-stage="${id}"]`);
    if (!item) return;
    const wasOpen = item.classList.contains('open');
    // Close all
    document.querySelectorAll('.timeline__item.open').forEach(el => el.classList.remove('open'));
    // Toggle
    if (!wasOpen) item.classList.add('open');
}

// ── QUIZ ENGINE ─────────────────────────────
let quizData = [];
let quizIndex = 0;
let quizScore = 0;
let quizAnswered = false;
let quizInitialized = false;

function initQuiz() {
    quizInitialized = true;
    quizIndex = 0;
    quizScore = 0;
    document.getElementById('quiz-results').classList.add('hidden');
    document.getElementById('quiz-card').classList.remove('hidden');
    document.getElementById('quiz-counter').classList.remove('hidden');
    document.querySelector('.quiz__progress').classList.remove('hidden');
    fetch('/api/quiz')
        .then(r => r.json())
        .then(data => { quizData = data; renderQuestion(); });
}

function renderQuestion() {
    if (quizIndex >= quizData.length) { showResults(); return; }
    quizAnswered = false;
    const q = quizData[quizIndex];
    const letters = ['A', 'B', 'C', 'D'];
    const progress = ((quizIndex) / quizData.length) * 100;
    document.getElementById('quiz-progress-bar').style.width = progress + '%';
    document.getElementById('quiz-counter').textContent = `Question ${quizIndex + 1} of ${quizData.length}`;

    let html = `<div class="quiz__question">${q.question}</div><div class="quiz__options">`;
    q.options.forEach((opt, i) => {
        html += `<div class="quiz__option" data-idx="${i}" onclick="selectAnswer(${q.id}, ${i})">
            <span class="quiz__option-letter">${letters[i]}</span>
            <span>${opt}</span>
        </div>`;
    });
    html += '</div>';
    document.getElementById('quiz-card').innerHTML = html;
}

function selectAnswer(qId, idx) {
    if (quizAnswered) return;
    quizAnswered = true;

    fetch('/api/quiz/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_id: qId, answer: idx })
    })
    .then(r => r.json())
    .then(data => {
        const options = document.querySelectorAll('.quiz__option');
        options.forEach(o => {
            const i = parseInt(o.dataset.idx);
            if (i === data.correct_answer) o.classList.add('correct');
            if (i === idx && !data.correct) o.classList.add('wrong');
        });
        if (data.correct) quizScore++;

        // Show explanation
        const card = document.getElementById('quiz-card');
        card.innerHTML += `<div class="quiz__explanation">💡 ${data.explanation}</div>`;
        card.innerHTML += `<div class="quiz__next-wrap"><button class="btn btn--primary" onclick="nextQuestion()">
            ${quizIndex < quizData.length - 1 ? 'Next Question →' : 'See Results →'}
        </button></div>`;
    });
}

function nextQuestion() {
    quizIndex++;
    renderQuestion();
}

function showResults() {
    document.getElementById('quiz-card').classList.add('hidden');
    document.getElementById('quiz-counter').classList.add('hidden');
    document.querySelector('.quiz__progress').classList.add('hidden');
    const results = document.getElementById('quiz-results');
    results.classList.remove('hidden');

    document.getElementById('quiz-progress-bar').style.width = '100%';
    document.getElementById('quiz-results-score').textContent = `${quizScore}/${quizData.length}`;

    // Animate circle
    const circumference = 2 * Math.PI * 54; // r=54
    const offset = circumference - (quizScore / quizData.length) * circumference;
    setTimeout(() => {
        document.getElementById('quiz-results-fill').style.strokeDashoffset = offset;
    }, 100);

    // Messages
    const pct = (quizScore / quizData.length) * 100;
    let title, msg;
    if (pct === 100) { title = '🏆 Perfect Score!'; msg = 'You have an excellent understanding of electoral systems. You\'re ready to teach others!'; }
    else if (pct >= 60) { title = '🎉 Great Job!'; msg = 'You have solid knowledge of elections. A few areas could use review — ask Claude for study tips!'; }
    else { title = '📚 Keep Learning!'; msg = 'Elections are complex! Use the timeline and glossary to strengthen your understanding, then try again.'; }
    document.getElementById('quiz-results-title').textContent = title;
    document.getElementById('quiz-results-msg').textContent = msg;
}

function restartQuiz() { initQuiz(); }

function getStudyTips() {
    const prompt = `I just scored ${quizScore} out of ${quizData.length} on an election process quiz. ` +
        `The topics covered were: FPTP voting, gerrymandering, proportional representation, hung parliaments, and the Electoral College. ` +
        `Based on my score, give me personalized study tips and resources to improve my understanding of electoral systems.`;
    openModal('Personalized Study Tips', `<p>Copy this prompt to ask Claude for personalized study recommendations based on your score:</p><div style="background:var(--surface-light);padding:16px;border-radius:10px;margin-top:12px;font-size:0.9rem;line-height:1.6;user-select:all;cursor:text;">${prompt}</div><p style="margin-top:12px;font-size:0.85rem;color:var(--text-muted);">💡 Tip: Select all the text above, copy it, and paste it into a new Claude conversation.</p>`);
}

// ── GLOSSARY SEARCH ─────────────────────────
const glossarySearch = document.getElementById('glossary-search');
if (glossarySearch) {
    glossarySearch.addEventListener('input', () => {
        const query = glossarySearch.value.toLowerCase().trim();
        const cards = document.querySelectorAll('.glossary__card');
        let visible = 0;
        cards.forEach(card => {
            const term = card.dataset.term;
            const match = term.includes(query) || card.querySelector('.glossary__card-def').textContent.toLowerCase().includes(query);
            card.style.display = match ? '' : 'none';
            if (match) visible++;
        });
        document.getElementById('glossary-empty').classList.toggle('hidden', visible > 0);
    });
}

// ── DEEP DIVE / PROMPTS ─────────────────────
function askDeepDive(prompt) {
    openModal('Deep Dive', `<p>Explore this topic further with AI:</p><div style="background:var(--surface-light);padding:16px;border-radius:10px;margin-top:12px;font-size:0.9rem;line-height:1.6;user-select:all;cursor:text;">${prompt}</div><p style="margin-top:12px;font-size:0.85rem;color:var(--text-muted);">💡 Copy the prompt above and paste it into Claude or your favorite AI assistant for a detailed explanation.</p>`);
}

function exploreGlossary(term) {
    const prompt = `Explain the election term "${term}" in comprehensive detail: its origin, how it works in practice, real-world examples, and why it matters for democracy.`;
    openModal(`Explore: ${term}`, `<p>Learn everything about <strong>${term}</strong>:</p><div style="background:var(--surface-light);padding:16px;border-radius:10px;margin-top:12px;font-size:0.9rem;line-height:1.6;user-select:all;cursor:text;">${prompt}</div><p style="margin-top:12px;font-size:0.85rem;color:var(--text-muted);">💡 Copy the prompt above and paste it into Claude for an in-depth exploration.</p>`);
}

function compareDeepDive(prompt) {
    openModal('Country Deep Dive', `<p>Get a comprehensive overview of this country's electoral system:</p><div style="background:var(--surface-light);padding:16px;border-radius:10px;margin-top:12px;font-size:0.9rem;line-height:1.6;user-select:all;cursor:text;">${prompt}</div><p style="margin-top:12px;font-size:0.85rem;color:var(--text-muted);">💡 Copy the prompt above and paste it into Claude for a full country analysis.</p>`);
}

function sendAskPrompt(prompt) {
    openModal('Ask Claude', `<p>Ready-to-use prompt for a deep conversation:</p><div style="background:var(--surface-light);padding:16px;border-radius:10px;margin-top:12px;font-size:0.9rem;line-height:1.6;user-select:all;cursor:text;">${prompt}</div><p style="margin-top:12px;font-size:0.85rem;color:var(--text-muted);">💡 Copy the prompt above and start a new Claude conversation for an in-depth discussion.</p>`);
}

function sendCustomPrompt() {
    const input = document.getElementById('custom-prompt-input');
    const val = input.value.trim();
    if (!val) { input.focus(); return; }
    openModal('Your Question', `<p>Your custom election question:</p><div style="background:var(--surface-light);padding:16px;border-radius:10px;margin-top:12px;font-size:0.9rem;line-height:1.6;user-select:all;cursor:text;">${val}</div><p style="margin-top:12px;font-size:0.85rem;color:var(--text-muted);">💡 Copy and paste this into Claude for a comprehensive answer.</p>`);
    input.value = '';
}

// ── MODAL ───────────────────────────────────
function openModal(title, bodyHtml) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-body').innerHTML = bodyHtml;
    document.getElementById('modal-overlay').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
    document.body.style.overflow = '';
}

// Close on Escape
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// ── CUSTOM PROMPT ENTER KEY ─────────────────
const customInput = document.getElementById('custom-prompt-input');
if (customInput) {
    customInput.addEventListener('keydown', e => { if (e.key === 'Enter') sendCustomPrompt(); });
}

// ── HERO SCROLL ─────────────────────────────
const heroScroll = document.querySelector('.hero__scroll-indicator');
if (heroScroll) {
    heroScroll.addEventListener('click', () => {
        document.getElementById('tabs').scrollIntoView({ behavior: 'smooth' });
    });
}

// ── TABS STICKY SHADOW ──────────────────────
const tabs = document.getElementById('tabs');
if (tabs) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > window.innerHeight - 100) {
            tabs.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
        } else {
            tabs.style.boxShadow = 'none';
        }
    });
}
