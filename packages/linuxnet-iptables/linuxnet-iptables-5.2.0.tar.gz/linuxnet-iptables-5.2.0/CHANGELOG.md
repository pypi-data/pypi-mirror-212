Change Log
==========

5.2.0 (2023-06-03)
------------------

- added NoTrackTarget class to support the iptables NOTRACK target
- added TraceTarget class to support the iptables TRACE target

5.0.4 (2023-03-05)
------------------

- bugfixes in ConnmarkTarget class

5.0.2 (2023-03-01)
------------------

- major version updated due to changes to the Chain class:
    * the Chain methods that were only applicable to builtin chains
      were moved to the new BuiltinChain class (which is a subclass
      of Chain)
    * the Chain.__init__() signature changed, however this does not
      affect code that only specified a chain name when creating a
      Chain instance
    * the Chain methods set_pft/clear_pft were renamed to
      _set_pft/_clear_pft
- added support for setting the policy of a builtin chain
- added support for the 'security' table

4.3.1 (2023-02-20)
------------------

- Added method to Chain/IptablesPacketFilterTable class to zero the packet/byte
  counters of a specific chain, or all chains

4.2.1 (2023-02-07)
------------------

- Fixed bug in LogTarget class

4.2.0 (2023-02-06)
------------------

- added framework for extending the linuxnet.iptables package
  with new xxxMatch and xxxTarget classes to support additional
  iptables match and target extensions
- added new section in the documentation with information
  on how to add new match/target classes (including examples)
- reworked package module structure:
    * monolithic match.py module broken into per-match-class modules
    * monolithic target.py module broken into per-target-class modules
- all CONNMARK target options are now supported
- added support for 'owner' match
- added mask support in MarkMatch and ConnmarkMatch classes
- the IcmpTypeCriterion now supports the complete list of ICMP types
  and ICMP codes
- The following changes were backwards-incompatible, and resulted
  in the bumpting of the major version number:
    * the xxxCriterion classes are no longer in the linuxnet.iptables
      namespace
    * the Criterion.equals() method is no longer implemented
    * the MssCriterion value changed from a string to a tuple of integers
    * the RateLimitCriterion value changed from integer to a
      LimitMatch.Rate object
    * the RateLimitCriterion rate2spec and spec2rate methods were removed
    * replaced the LogTarget.set_log_options() method with
      option-specific methods

3.2.0 (2023-01-27)
------------------

- Improved MARK/CONNMARK target support
- Reworked documentation

3.1.0 (2023-01-21)
------------------

- Added support for the TTL target
- Added support for the TTL match

3.0.1 (2022-12-31)
------------------

- First published release

