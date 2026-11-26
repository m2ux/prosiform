# Generated First

The two sources are byte-identical. Both authored and generated sections display Investigate.

| Build | Source | Result |
| --- | --- | --- |
| Before F42 | [Guide](before/source/guide.md) · [Dispatched target](before/source/investigate.md) | [E_HEADING_COLLISION; no bundle](before/result.md) |
| With F42 | [Guide](after/source/guide.md) · [Dispatched target](after/source/investigate.md) | [Guide bundle](after/bundles/guide.bundles/guide.bundle.md) · [Child bundle](after/bundles/guide.bundles/investigate.bundle.md) |

The dispatched link and Intake graph node point to #investigate. The ordinary link and Authored graph node point to #investigate-1. The brief's Inputs link remains local to its own content.

[Before receipt](before/receipt.json) · [After receipt](after/receipt.json)
