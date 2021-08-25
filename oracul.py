from task import (BACKLOG, TASK_PERFORM_LOG, Task, TaskPerform, TaskStatus,
                  clear_enviroment)


class Oracul:
    def predict(self, tags, performers):
        similar_tasks_by_tags = set()
        for task in BACKLOG.values():
            if task.status == TaskStatus.DONE and task.tags == tags:
                similar_tasks_by_tags.add(task.task_id)

        if len(similar_tasks_by_tags) == 0:
            return {}

        similar_tasks_by_performers = set()
        for record in TASK_PERFORM_LOG.values():
            if record.performer_id in performers:
                similar_tasks_by_performers.add(record.task_id)

        if len(similar_tasks_by_performers) == 0:
            return {}

        similar_tasks = similar_tasks_by_tags.intersection(
            similar_tasks_by_performers)

        prediction = 0.0
        for record in TASK_PERFORM_LOG.values():
            if record.task_id in similar_tasks:
                prediction += record.total_time_spent
        prediction /= float(len(similar_tasks))

        return {99: prediction}
