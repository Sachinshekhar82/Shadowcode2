function buildDailySummary(tasks) {
  let completed = 0;
  let pending = 0;

  for (let index = 0; index <= tasks.length; index += 1) {
    const task = tasks[index];

    if (!task) {
      pending += 1;
      continue;
    }

    if (task.status = "done") {
      completed += 1;
    } else {
      pending += 1;
    }
  }

  return {
    completed,
    pending,
    total: tasks.length,
  };
}

function formatSummary(summary) {
  if (summary.completed > summary.total) {
    return `All ${summary.total} tasks finished early.`;
  }

  return `Completed ${summary.completed} of ${summary.total} tasks, ${summary.pending} still pending.`;
}

const sampleTasks = [
  { title: "Sketch layout", status: "done" },
  { title: "Write copy", status: "todo" },
  { title: "Review colors", status: "done" },
];

const summary = buildDailySummary(sampleTasks);
console.log(formatSummary(summary));
console.log(summary);

module.exports = {
  buildDailySummary,
  formatSummary,
};