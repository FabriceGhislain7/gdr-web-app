const analyticsBootstrap = document.getElementById('analytics-bootstrap');
const analyticsApiUrl = analyticsBootstrap?.dataset?.apiUrl || '';
const noRiskText = analyticsBootstrap?.dataset?.noRiskText || 'No high-risk users detected.';
const filterMetaTemplate = analyticsBootstrap?.dataset?.filterMetaTemplate || 'Showing {filtered} of {total} players';
let currentPayload = {};

try {
  currentPayload = JSON.parse(analyticsBootstrap?.textContent || '{}');
} catch (error) {
  currentPayload = {};
}

let chartRefs = {};
const palette = ['#0ea5e9', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#14b8a6', '#eab308', '#64748b', '#ec4899', '#10b981'];
const paletteSoft = ['rgba(14,165,233,.65)', 'rgba(34,197,94,.65)', 'rgba(245,158,11,.65)', 'rgba(239,68,68,.65)', 'rgba(139,92,246,.65)', 'rgba(20,184,166,.65)', 'rgba(234,179,8,.65)', 'rgba(100,116,139,.65)', 'rgba(236,72,153,.65)', 'rgba(16,185,129,.65)'];

function bar(id, labels, values) {
  if (chartRefs[id]) chartRefs[id].destroy();
  chartRefs[id] = new Chart(document.getElementById(id), {
    type: 'bar',
    data: { labels, datasets: [{ data: values, backgroundColor: paletteSoft, borderColor: palette, borderWidth: 1 }] },
    options: { responsive: true, maintainAspectRatio: true, aspectRatio: 2.2, plugins: { legend: { display: false } } }
  });
}

function doughnut(id, labels, values) {
  if (chartRefs[id]) chartRefs[id].destroy();
  chartRefs[id] = new Chart(document.getElementById(id), {
    type: 'doughnut',
    data: { labels, datasets: [{ data: values, backgroundColor: palette }] },
    options: { responsive: true, maintainAspectRatio: true, aspectRatio: 1.8 }
  });
}

function renderTables(payload) {
  const tables = payload.tables || {};
  if (!Object.keys(tables).length) return;
  const playtime = tables.top_playtime || [];
  const spenders = tables.top_spenders || [];
  const risk = tables.high_risk_users || [];
  document.getElementById('tablePlaytime').innerHTML = playtime.map((p) => `<tr><td>${p.nome}</td><td>${p.classe}</td><td>${p.ore}</td></tr>`).join('');
  document.getElementById('tableSpenders').innerHTML = spenders.map((p) => `<tr><td>${p.nome}</td><td>EUR ${p.spesa_mensile}</td><td>${p.abbonato}</td></tr>`).join('');
  document.getElementById('tableRisk').innerHTML = risk.length
    ? risk.map((p) => `<tr><td>${p.nome}</td><td>${p.soddisfazione}</td><td>${p.crash}</td></tr>`).join('')
    : `<tr><td colspan="3" class="text-muted">${noRiskText}</td></tr>`;
}

function renderAlerts(payload) {
  const wrap = document.getElementById('alertsWrap');
  const list = document.getElementById('alertsList');
  if (!wrap || !list) return;
  const alerts = payload.alerts || [];
  if (!alerts.length) {
    wrap.classList.add('d-none');
    list.innerHTML = '';
    return;
  }
  wrap.classList.remove('d-none');
  list.innerHTML = alerts.map((a) => `<li>${a}</li>`).join('');
}

function renderKpis(payload) {
  const k = payload.kpis || {};
  if (!Object.keys(k).length) return;
  document.getElementById('kpiPlayers').textContent = k.total_players ?? 0;
  document.getElementById('kpiHours').textContent = k.total_playtime_hours ?? 0;
  document.getElementById('kpiWinrate').textContent = `${k.win_rate ?? 0}%`;
  document.getElementById('kpiRevenue').textContent = `EUR ${k.monthly_revenue ?? 0}`;
  document.getElementById('kpiArpu').textContent = `EUR ${k.arpu ?? 0}`;
  document.getElementById('kpiSubs').textContent = `${k.subscriber_rate ?? 0}%`;
  document.getElementById('kpiSession').textContent = `${k.avg_session_minutes ?? 0} min`;
  document.getElementById('kpiSat').textContent = `${k.avg_satisfaction ?? 0}/10`;
}

function renderCharts(payload) {
  const c = payload.charts || {};
  if (!c.class_distribution || typeof Chart === 'undefined') return;
  bar('classChart', c.class_distribution.labels, c.class_distribution.values);
  doughnut('clusterChart', c.cluster_distribution.labels, c.cluster_distribution.values);
  doughnut('deviceChart', c.device_distribution.labels, c.device_distribution.values);
  bar('acqChart', c.acquisition_distribution.labels, c.acquisition_distribution.values);
  bar('dayChart', c.active_day_distribution.labels, c.active_day_distribution.values);
  doughnut('satBandChart', c.satisfaction_bands.labels, c.satisfaction_bands.values);
  bar('satClassChart', c.satisfaction_by_class.labels, c.satisfaction_by_class.values);
  bar('spendClusterChart', c.spend_by_cluster.labels, c.spend_by_cluster.values);
  bar('crashDeviceChart', c.crash_by_device.labels, c.crash_by_device.values);
}

function renderAll(payload) {
  if (!payload || !Object.keys(payload).length) return;
  renderKpis(payload);
  renderAlerts(payload);
  renderTables(payload);
  renderCharts(payload);
  const metaEl = document.getElementById('filterMeta');
  if (payload.meta) {
    metaEl.textContent = filterMetaTemplate
      .replace('{filtered}', payload.meta.filtered_count)
      .replace('{total}', payload.meta.total_count);
  }
  else metaEl.textContent = '';
}

async function fetchFiltered() {
  if (!analyticsApiUrl) return;
  const params = new URLSearchParams({
    classe_personaggio: document.getElementById('filterClasse').value,
    genere: document.getElementById('filterGenere').value,
    paese: document.getElementById('filterPaese').value,
    tipo_dispositivo: document.getElementById('filterDevice').value,
    cluster_comportamentale: document.getElementById('filterCluster').value
  });

  try {
    const res = await fetch(`${analyticsApiUrl}?${params.toString()}`);
    if (!res.ok) return;
    currentPayload = await res.json();
    renderAll(currentPayload);
  } catch (error) {
    // Keep server-rendered values if the API call fails.
  }
}

document.getElementById('applyFilters')?.addEventListener('click', fetchFiltered);
document.getElementById('resetFilters')?.addEventListener('click', () => {
  document.getElementById('filterClasse').value = '';
  document.getElementById('filterGenere').value = '';
  document.getElementById('filterPaese').value = '';
  document.getElementById('filterDevice').value = '';
  document.getElementById('filterCluster').value = '';
  fetchFiltered();
});

if (currentPayload && currentPayload.kpis && Object.keys(currentPayload.kpis).length) {
  renderAll(currentPayload);
} else {
  fetchFiltered();
}


