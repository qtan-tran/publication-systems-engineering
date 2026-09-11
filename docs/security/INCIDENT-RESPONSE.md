# Incident Response Guidance

This document is operational guidance, not a substitute for an organization's incident-response plan.

If an unpublished artifact is suspected to have leaked:

1. preserve the suspected file and its hash;
2. identify whether it is a draft, proof, or release artifact;
3. if it is a PSE proof, compare the visible proof ID and checksum with private proof manifests;
4. preserve relevant repository/build/access logs;
5. revoke compromised credentials or sharing links in the downstream infrastructure;
6. determine whether other recipient-specific proofs or source repositories were exposed;
7. follow contractual, privacy, employment, and legal reporting obligations applicable to the publisher.

Do not destroy provenance manifests merely because a proof was leaked; they may be necessary to investigate the event.
