# Project

**The OSDI 2025 artifact is located in the `osdi25/` directory. Please see the `osdi25-artifact` branch for the most up-to-date version of the artifact.**

This repository contains code for verified storage systems. The code is
written in, and its correctness properties are verified with,
[Verus](https://github.com/verus-lang/verus).

This project contains the following: 

* `osdi25` contains the artifact for our OSDI 2025 paper, "PoWER Never Corrupts: 
  Tool-Agnostic Verification of Crash Consistency and Corruption Detection". 
  It contains the verified persistent-memory key-value store CapybaraKV, the 
  verified notary service CapybaraNS, and instructions how to run/verify these 
  systems and how to check all associated proofs.
* `pmemlog` implements an append-only log on persistent memory. The
  implementation handles crash consistency, ensuring that even if the process
  or machine crashes, it acts like an append-only log across the crashes. It
  also handles bit corruption, detecting if metadata read from persistent
  memory is corrupted.
* `storage_node` is an in-progress persistent memory key-value store. Its structure 
  is further described in its [README](storage_node/README.md).
* `unverified` contains unverified mocks and tests related to the `storage_node` key value store. 
* `deps_hack` contains unverified dependencies that are imported by `storage_node`.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
