// Lightweight interactivity for the Excel Life Game
// - Timer
// - Quiz gating to enable Next
// - Progress bar update
// - Ranking highlight
// - Hints toggle (press "h")

(function () {
  document.addEventListener('DOMContentLoaded', () => {
    initTimer();
    initQuiz();
    initProgress();
    initRankingHighlight();
    initGlobalNextGuard();
    initHintsToggle();
  });

  function initTimer() {
    const el = document.querySelector('[data-js="timer"]');
    if (!el) return;
    const key = `timer:${location.pathname}`;
    let start = Number(sessionStorage.getItem(key));
    if (!start) {
      start = Date.now();
      sessionStorage.setItem(key, String(start));
    }
    const fmt = (secs) => {
      const m = Math.floor(secs / 60)
        .toString()
        .padStart(2, '0');
      const s = (secs % 60).toString().padStart(2, '0');
      return `${m}:${s}`;
    };
    const tick = () => {
      const secs = Math.floor((Date.now() - start) / 1000);
      el.textContent = fmt(secs);
    };
    tick();
    setInterval(tick, 1000);
  }

  function initQuiz() {
    const forms = document.querySelectorAll('[data-js="quiz"]');
    forms.forEach((form) => {
      const correct = (form.dataset.correct || '').trim();
      const feedback = form.querySelector('[data-js="feedback"]');
      const next = form.querySelector('[data-js="next"]') || document.querySelector('[data-js="next"]') || document.querySelector('.btn-next');
      if (next) disableNext(next, true);

      form.addEventListener('change', () => {
        const chosen = form.querySelector('input[type="radio"]:checked');
        const ok = chosen && chosen.value === correct;
        form.classList.toggle('is-correct', !!ok);
        form.classList.toggle('is-wrong', !!chosen && !ok);
        if (feedback) {
          feedback.textContent = ok ? 'Correto! ✅' : '';
        }
        if (next) disableNext(next, !ok);
      });
    });
  }

  function initGlobalNextGuard() {
    document.addEventListener('click', (ev) => {
      const t = ev.target;
      if (!(t instanceof Element)) return;
      const next = t.closest('[data-js="next"], .btn-next');
      if (!next) return;
      if (next.classList.contains('is-disabled') || next.getAttribute('aria-disabled') === 'true') {
        ev.preventDefault();
        ev.stopPropagation();
      }
    });
  }

  function disableNext(el, disabled) {
    if (!el) return;
    if (disabled) {
      el.classList.add('is-disabled');
      el.setAttribute('aria-disabled', 'true');
      // keep href but block via click guard; visually show disabled
    } else {
      el.classList.remove('is-disabled');
      el.removeAttribute('aria-disabled');
    }
  }

  function initProgress() {
    document.querySelectorAll('[data-js="progress"]').forEach((wrap) => {
      const step = Number(wrap.getAttribute('data-step')) || 0;
      const total = Number(wrap.getAttribute('data-total')) || 0;
      const pct = total > 0 ? Math.min(100, Math.max(0, Math.round((step / total) * 100))) : 0;
      const bar = wrap.querySelector('.progress__bar');
      if (bar) bar.style.width = pct + '%';
      const label = wrap.querySelector('.progress__label');
      if (label) label.textContent = total ? `Etapa ${step} de ${total} · ${pct}%` : '';
    });
  }

  function initRankingHighlight() {
    const list = document.querySelector('[data-js="ranking"]');
    if (!list) return;
    const username = (list.getAttribute('data-username') || '').trim();
    if (!username) return;
    Array.from(list.querySelectorAll('li')).forEach((li) => {
      const txt = li.textContent || '';
      if (txt.trim().startsWith(username + ' ') || txt.includes(` ${username} `) || txt.includes(`${username} —`) || txt.includes(`${username} -`)) {
        li.classList.add('me');
      }
    });
  }

  function initHintsToggle() {
    document.addEventListener('keydown', (e) => {
      if (e.key.toLowerCase() === 'h') {
        document.body.classList.toggle('hints-hidden');
      }
    });
  }
})();
