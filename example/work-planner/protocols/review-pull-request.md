---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Review Pull Request

The draft pull request and body that present one epic base's delivered changes for review.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md).

## Procedure

1. **Find.**
   Use the review number in the supplied delivery findings.
   - When it is absent:
     - Apply [Locate Review Pull Request](../artifacts/pull-request.md#locate-review-pull-request) with the repository and epic base as head.
     - Use its returned number or absence result.
   - Fetch an existing review through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state).
2. **Populate.**
   Pass the existing body when present and the actual task merges into the base to [Populate Review Body](../artifacts/pull-request-body.md#populate-review-body).
3. **Publish.**
   For an existing review, or a base whose [State](../artifacts/pull-request.md#state) calls for one, pass the returned file to [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request).
   - For an existing review, supply its number.
   - For a new review, supply the epic kind, the epic base as head with the target [Other Pull Requests](../artifacts/pull-request.md#other-pull-requests) gives it, the epic's issue, the repository setting the caller confirmed and a link-snapshot destination.
   - Return a discrepancy Publish Pull Request reports to the caller.
   - When the base has no review and its State calls for none, return the absence result to the caller.
4. **Record.**
   Apply [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with the current epic and the task-merge records, including the review state Publish Pull Request returned.
   - Return its updated body and [Delivery Findings](../artifacts/epic.md#delivery-findings) with the review identity to the caller.
