document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/horarios')
        .then(response => response.json())
        .then(data => renderTable(data))
        .catch(err => console.error('Erro ao carregar dados:', err));
});

function renderTable(data) {
    const thead = document.getElementById('table-header');
    const tbody = document.getElementById('table-body');

    // Função auxiliar para converter "HH:MM" em minutos totais
    const toMinutes = (timeStr) => {
        const [h, m] = timeStr.trim().split(':').map(Number);
        return (h * 60) + m;
    };

    // 1. Processar as linhas base da tabela
    const gridIntervals = data.horarios.map(h => {
        // Expressão regular tolerante a hifens normais e traços compridos (en-dash)
        const parts = h.split(/\s*[-–]\s*/); 
        return {
            label: h,
            start: toMinutes(parts[0]),
            end: toMinutes(parts[1])
        };
    });

    // 2. Mapear as aulas usando o Dia e o Horário de Início (em minutos)
    const mapaAulas = {};
    data.aulas.forEach(aula => {
        const parts = aula.horario.split(/\s*[-–]\s*/);
        const startMin = toMinutes(parts[0]);
        const endMin = toMinutes(parts[1]);

        if (!mapaAulas[aula.dia]) mapaAulas[aula.dia] = {};

        // Calcula quantos blocos da tabela essa aula engloba
        let span = 0;
        gridIntervals.forEach(interval => {
            if (interval.start >= startMin && interval.end <= endMin) {
                span++;
            }
        });

        mapaAulas[aula.dia][startMin] = { ...aula, rowSpan: span };
    });

    // 3. Preencher cabeçalho de dias
    data.dias.forEach(dia => {
        const th = document.createElement('th');
        th.setAttribute('scope', 'col');
        th.textContent = dia;
        thead.appendChild(th);
    });

    // 4. Estado para controlar o rowspan (quantas células pular por coluna nas próximas iterações)
    const skipCells = {};
    data.dias.forEach(dia => skipCells[dia] = 0);

    // 5. Preencher o corpo da tabela
    gridIntervals.forEach(interval => {
        const tr = document.createElement('tr');

        // Coluna de horário
        const thRow = document.createElement('th');
        thRow.setAttribute('scope', 'row');
        thRow.textContent = interval.label;
        tr.appendChild(thRow);

        // Colunas de cada dia
        data.dias.forEach(dia => {

            // Se estamos no meio de um bloco mesclado (rowspan), diminuímos o contador e pulamos a criação do <td>
            if (skipCells[dia] > 0) {
                skipCells[dia]--;
                return;
            }

            const aula = mapaAulas[dia]?.[interval.start];

            if (aula && aula.rowSpan > 0) {
                const td = document.createElement('td');
                td.classList.add('ocupado');

                if (aula.rowSpan > 1) {
                    td.rowSpan = aula.rowSpan;
                }

                const localHtml = /^https?:\/\//.test(aula.local)
                    ? `<a href="${aula.local}" target="_blank" rel="noopener">${aula.local.includes('discord') ? 'Discord' : 'Link'}</a>`
                    : aula.local;

                td.innerHTML = `
                    <span class="materia">${aula.materia}</span>
                    <span class="monitor">Monitor: ${aula.monitor}</span>
                    <span class="local">${localHtml}</span>
                `;
                tr.appendChild(td);

                // Informa o sistema para pular as células das próximas X linhas neste dia
                skipCells[dia] = aula.rowSpan - 1;
            } else {
                const td = document.createElement('td');
                td.className = 'vago';
                td.textContent = '—';
                tr.appendChild(td);
            }
        });

        tbody.appendChild(tr);
    });
}