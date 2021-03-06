from oracul import Oracul
from task import (BACKLOG, Task, TaskPerform, TaskStatus,
                  clear_enviroment, new_task, new_task_perform)


def test_prediction1():
    clear_enviroment()

    new_task(Task("#task_id1", {"tag1", "tag2", "tag3"}, TaskStatus.DONE))

    new_task_perform(TaskPerform("#performer_id1", "#task_id1", 10.5))
    new_task_perform(TaskPerform("#performer_id2", "#task_id1", 6.0))

    oracul = Oracul()
    prediction = oracul.predict({"tag1", "tag2", "tag3"},
                                {"#performer_id1", "#performer_id2"})

    expected = 10.5 + 6.0
    assert prediction[99] == expected


def test_prediction2():
    clear_enviroment()

    new_task(Task("#task_id1", {"tag1", "tag2", "tag3"}, TaskStatus.DONE))
    new_task(Task("#task_id2", {"tag1", "tag2", "tag3"}, TaskStatus.DONE))

    new_task_perform(TaskPerform("#performer_id1", "#task_id1", 10.5))
    new_task_perform(TaskPerform("#performer_id2", "#task_id1", 6.0))

    new_task_perform(TaskPerform("#performer_id1", "#task_id2", 10.5 / 2.0))
    new_task_perform(TaskPerform("#performer_id2", "#task_id2", 6.0 / 2.0))

    oracul = Oracul()
    prediction = oracul.predict({"tag1", "tag2", "tag3"},
                                {"#performer_id1", "#performer_id2"})

    expected = ((10.5 + 6.0) + (10.5 + 6.0) / 2.0) / 2.0
    assert prediction[99] == expected


def test_prediction3():
    clear_enviroment()

    task1 = new_task(Task("#task_id1", {"tag1", "tag2", "tag3"}, TaskStatus.DONE))
    task2 = new_task(Task("#task_id2", {"tag1", "tag2", "tag3"}, TaskStatus.DONE))

    new_task_perform(TaskPerform("#performer_id1", "#task_id1", 10.5))
    new_task_perform(TaskPerform("#performer_id2", "#task_id1", 6.0))

    new_task_perform(TaskPerform("#performer_id3", "#task_id2", 10.5 / 2.0))

    oracul = Oracul()
    prediction1 = oracul.predict({"tag1", "tag2", "tag3"},
                                 {"#performer_id1", "#performer_id2"})
    expected1 = 10.5 + 6.0
    assert prediction1[99] == expected1

    prediction2 = oracul.predict({"tag1", "tag2", "tag3"},
                                 {"#performer_id3"})
    expected2 = 10.5 / 2.0
    assert prediction2[99] == expected2

    prediction3 = oracul.predict({"tag1", "tag2"},
                                 {"#performer_id3"})
    assert prediction3 == {}


def test_prediction4():
    clear_enviroment()

    task1 = new_task(Task("#task_id1", {"tag1", "tag2", "tag3"}, TaskStatus.NEW))
    task2 = new_task(Task("#task_id2", {"tag1", "tag2", "tag3"}, TaskStatus.IN_PROGRESS))

    new_task_perform(TaskPerform("#performer_id1", "#task_id1", 10.5))
    new_task_perform(TaskPerform("#performer_id2", "#task_id1", 6.0))

    new_task_perform(TaskPerform("#performer_id3", "#task_id2", 10.5 / 2.0))

    oracul = Oracul()
    prediction1 = oracul.predict({"tag1", "tag2", "tag3"},
                                 {"#performer_id1", "#performer_id2"})
    assert prediction1 == {}

    prediction2 = oracul.predict({"tag1", "tag2", "tag3"},
                                 {"#performer_id3"})
    assert prediction2 == {}
