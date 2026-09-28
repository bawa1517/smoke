# Taskwell

This context records Taskwell's domain language so the browser app and its planned API contract use the same terms.

## Language

**Task**:
An item in the Taskwell user's to-do list, described by its text and whether it is complete. It has an identifier the client uses to refer to it.
_Avoid_: To-do, work item

**Task ID**:
A positive integer supplied by the client to identify one Task; the ID does not change after creation. The current browser app uses a numeric timestamp.
_Avoid_: Task key, task number
