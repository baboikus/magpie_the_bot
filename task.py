from enum import Enum
from threading import Lock, Timer

import utils

# TODO move global state interaction to abstract api
# TODO add sqlite support(and manual heroku test!)
BACKLOG = {}
TASK_PERFORM_LOG = {}
SESSIONS = {}
EVENTS_LOG = {}

EVENT_HANDLERS = {}
MAILBOX = []

SEND_MESSAGE_TO = {}

ENVIRONMENT_MUTEX = Lock()


def run_atomic_state_action(action, args=None):
    ENVIRONMENT_MUTEX.acquire(1)
    try:
        r = None
        if args is None:
            r = action()
        elif len(args) == 1:
            r = action(args[0])
        elif len(args) == 2:
            r = action(args[0], args[1])
        elif len(args) == 3:
            r = action(args[0], args[1], args[2])
        ENVIRONMENT_MUTEX.release()
        return r
    except Exception as e:
        ENVIRONMENT_MUTEX.release()
        raise e


def new_task(task):
    BACKLOG[task.task_id] = task


def new_task_perform(perform):
    TASK_PERFORM_LOG[(perform.task_id, perform.performer_id)] = perform


def is_task_perform_exists(task_id, performer_id):
    return (task_id, performer_id) in TASK_PERFORM_LOG

def fetch_all_tasks_performs():
    return TASK_PERFORM_LOG.values()

def fetch_task_perform(task_id, performer_id):
    return TASK_PERFORM_LOG[(task_id, performer_id)]

def is_have_any_sessions():
    return len(SESSIONS) > 0

def new_session(task_id, performer_id):
    if task_id in SESSIONS:
        SESSIONS[task_id].add(performer_id)
    else:
        SESSIONS[task_id] = {performer_id}

def new_task_session(task_id):
    SESSIONS[task_id] = set()

def fetch_all_task_sessions(task_id):
    return SESSIONS.get(task_id, set())

def remove_session(task_id, performer_id):
    SESSIONS[task_id].remove(performer_id)
    if len(SESSIONS[task_id]) == 0:
        del SESSIONS[task_id]

def is_task_have_sessions(task_id):
    return task_id in SESSIONS and len(SESSIONS[task_id]) > 0

def is_session_exist(task_id, performer_id):
    return task_id in SESSIONS and performer_id in SESSIONS[task_id]

def new_event(task_id, event):
    if task_id in EVENTS_LOG:
        EVENTS_LOG[task_id] += [event]
    else:
        EVENTS_LOG[task_id] = [event]

def fetch_task_events(task_id):
    return EVENTS_LOG.get(task_id, [])

def new_mail(user_id, message):
    global MAILBOX
    MAILBOX += [(user_id, message)]


class EventType(Enum):
    CRUNCH = 0


def clear_enviroment():
    def action():
        BACKLOG.clear()
        TASK_PERFORM_LOG.clear()
        SESSIONS.clear()
        EVENTS_LOG.clear()
        EVENT_HANDLERS.clear()
        MAILBOX.clear()

    run_atomic_state_action(action)


def update_enviroment_loop():
    Timer(60.0, update_enviroment_loop).start()
    run_time_machine(1.0 / 60.0)


def update_mailbox_loop():
    def action():
        for adress, message in MAILBOX:
            if adress in SEND_MESSAGE_TO:
                print("sending message to % s: % s" % (adress, message))
                SEND_MESSAGE_TO[adress](message)
            else:
                print(
                    "no adress for % s. can't send message '% s'." %
                    (adress, message))
        MAILBOX.clear()

    run_atomic_state_action(action)

    Timer(10.0, update_mailbox_loop).start()


def run_time_machine(hours):
    if hours <= 0:
        return

    def action():
        in_progress = set()
        for task in BACKLOG.values():
            if task.status == TaskStatus.IN_PROGRESS:
                in_progress.add(task.task_id)

        for task_id, performer_id in TASK_PERFORM_LOG.keys():
            if task_id in in_progress:
                perform = fetch_task_perform(task_id, performer_id)
                if perform.performer_id in SESSIONS[perform.task_id]:
                    perform.total_time_spent += hours
                    perform.sessions_time_spent[-1] += hours

        if EventType.CRUNCH in EVENT_HANDLERS:
            for perform in TASK_PERFORM_LOG.values():
                if perform.sessions_time_spent[-1] > 8.0:
                    EVENT_HANDLERS[EventType.CRUNCH](perform)
    run_atomic_state_action(action)


def backlog_len(): return len(BACKLOG)
def fetch_task(task_id): return BACKLOG[task_id]
def fetch_all_tasks(): return BACKLOG.values()
def fetch_all_tasks_ids(): return BACKLOG.keys()


class TaskStatus(Enum):
    UNKNOWN = 1
    NEW = 2
    IN_PROGRESS = 3
    SUSPENDED = 4
    DONE = 5

# TODO get rid of global state modifications inside __init__ methods


class Task:
    # TODO change task_id to id
    def __init__(self, task_id, tags, status):
        self.task_id = task_id
        self.tags = tags
        self.status = status

    def __eq__(self, other):
        return self.task_id == other.task_id \
            and self.tags == other.tags \
            and self.status == other.status

    def __repr__(self):
        return "Task id:% s tags:% s status:% s" % (
            self.task_id, self.tags, self.status)

    def tags_str(self):
        return utils.make_sorted_str(self.tags)

# TODO add UTC time data to sessions


class TaskPerform:
    # TODO switch performer_id and task_id places
    def __init__(self, performer_id, task_id, total_time_spent,
                 sessions_time_spent=None):
        self.performer_id = performer_id
        self.task_id = task_id
        self.total_time_spent = total_time_spent
        if sessions_time_spent is None:
            self.sessions_time_spent = [total_time_spent]
        else:
            self.sessions_time_spent = sessions_time_spent

    def __repr__(self):
        return "TaskPerform performer_id:% s task_id:% s total_time_spent:% s sessions_time_spent: % s" \
            % (self.performer_id, self.task_id, self.total_time_spent, self.sessions_time_spent)

    def __eq__(self, other):
        return self.performer_id == other.performer_id \
            and self.task_id == other.task_id \
            and self.total_time_spent == other.total_time_spent \
            and self.sessions_time_spent == other.sessions_time_spent
