(function() {
    const refreshBtn = document.getElementById('refreshBtn');
    const statusMsg = document.getElementById('statusMsg');
    const updateTime = document.getElementById('updateTime');
    const articleList = document.getElementById('articleList');
    const digestSummary = document.getElementById('digestSummary');
    const newsCount = document.getElementById('newsCount');

    function setCurrentTime() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        updateTime.textContent = `сегодня в ${hours}:${minutes}`;
    }

    const digestVariants = [
        '<strong>🔥 Главное за час:</strong><br>DeepSeek обошёл ChatGPT по качеству кода в бенчмарках.<br>GitHub Copilot получил поддержку Claude 3.5.<br>Вышла новая версия Django 5.1 с улучшенной асинхронностью.',
        '<strong>🔥 Главное за час:</strong><br>Релиз Python 3.13 с экспериментальным JIT-компилятором.<br>Microsoft представила новый инструмент для разработчиков AI.<br>В Redis обнаружена уязвимость, выпущено обновление.',
        '<strong>🔥 Главное за час:</strong><br>OpenAI и Google заключили партнёрство по стандартам AI-безопасности.<br>Вышел Django 4.2.16 с исправлением багов.<br>Новый фреймворк от JetBrains для веб-разработки.'
    ];

    const articleSets = [
        [
            { title: 'DeepSeek обогнал ChatGPT в бенчмарках кода', source: 'Habr', time: '15:10', tags: ['#AI', '#DeepSeek'] },
            { title: 'GitHub Copilot + Claude 3.5: что нового', source: 'Dev.to', time: '14:45', tags: ['#GitHub', '#AI'] },
            { title: 'Django 5.1: асинхронность стала быстрее', source: 'Django Blog', time: '13:30', tags: ['#Django', '#Python'] },
            { title: 'Microsoft представила AI Toolkit для VS Code', source: 'MS Dev', time: '12:50', tags: ['#Microsoft', '#AI'] }
        ],
        [
            { title: 'Python 3.13: JIT-компилятор и новые фичи', source: 'Python.org', time: '16:00', tags: ['#Python', '#JIT'] },
            { title: 'Redis 8.0: уязвимость исправлена', source: 'Redis Blog', time: '15:20', tags: ['#Redis', '#Security'] },
            { title: 'Microsoft AI Toolkit для разработчиков', source: 'MS Dev', time: '14:10', tags: ['#Microsoft', '#AI'] }
        ],
        [
            { title: 'OpenAI и Google договорились о безопасности AI', source: 'TechCrunch', time: '17:30', tags: ['#AI', '#Safety'] },
            { title: 'Django 4.2.16: патч для критических багов', source: 'Django Blog', time: '16:45', tags: ['#Django', '#Security'] },
            { title: 'JetBrains представил новый веб-фреймворк', source: 'JetBrains', time: '15:55', tags: ['#JetBrains', '#Web'] },
            { title: 'Google обновил Project Agent до версии 2.0', source: 'Google AI', time: '14:20', tags: ['#Google', '#AI'] }
        ]
    ];

    function handleRefresh() {
        refreshBtn.disabled = true;
        refreshBtn.innerHTML = '<span>⏳</span> Загрузка...';

        statusMsg.className = 'status-message loading';
        statusMsg.textContent = '⏳ Парсим новости, подождите...';

        setTimeout(function() {
            setCurrentTime();

            const randomIndex = Math.floor(Math.random() * digestVariants.length);
            digestSummary.innerHTML = digestVariants[randomIndex];

            const articles = articleSets[randomIndex % articleSets.length];
            let html = '';
            articles.forEach(function(article) {
                const tagsHtml = article.tags.map(t => `<span class="tag">${t}</span>`).join('');
                html += `
                    <div class="article-card">
                        <a href="#" target="_blank">${article.title}</a>
                        <div class="article-meta">
                            <span class="source">${article.source}</span>
                            <span>•</span>
                            <span>${article.time}</span>
                            ${tagsHtml}
                        </div>
                    </div>
                `;
            });
            articleList.innerHTML = html;

            const count = articles.length;
            const word = count % 10 === 1 && count % 100 !== 11 ? 'новость' : 
                        (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20) ? 'новости' : 'новостей');
            newsCount.textContent = `${count} ${word}`;

            articleList.style.opacity = '0.4';
            setTimeout(() => {
                articleList.style.opacity = '1';
                articleList.style.transition = 'opacity 0.3s';
            }, 150);

            statusMsg.className = 'status-message success';
            statusMsg.textContent = '✅ Дайджест обновлён!';

            refreshBtn.disabled = false;
            refreshBtn.innerHTML = '<span>⟳</span> Обновить дайджест';

            setTimeout(function() {
                statusMsg.className = 'status-message';
                statusMsg.textContent = '✅ Готов к работе';
            }, 5000);

        }, 3000);
    }

    refreshBtn.addEventListener('click', handleRefresh);
    setCurrentTime();

    console.log('✅ IT-Дайджест в Soft Purple стиле загружен!');
    console.log('🎨 Палитра: #564787, #DBCBD8, #F2FDDF');
})();