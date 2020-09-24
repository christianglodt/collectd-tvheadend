# Collectd plugin for Tvheadend

`collectd-tvheadend` is a simple Python3-based [collectd](https://collectd.org)
plugin for gathering statistics from [Tvheadend](https://tvheadend.org).

It gathers input-related statistics as documented [here](https://github.com/dave-p/TVH-API-docs/wiki/status#statusinputs).

## Installation

Clone this repository into a suitable directory.

Create the configuration file `/etc/collectd/collectd.conf.d/tvheadend.conf`
as follows and adapt it to your specific situation:
```
LoadPlugin python
&lt;Plugin python&gt;
    ModulePath "/path/to/collectd-tvheadend"
    LogTraces true
    Interactive false
    Import "collectd_tvheadend"
    &lt;Module collectd_tvheadend&gt;
        # Base url of Tvheadend:
        BaseURL "http://localhost:9981"
        # Add an HTTP header to the request (eg. for authentication):
        # Header "Cookie" "foo=bar"
    &lt;/Module&gt;
&lt;/Plugin&gt;
```
