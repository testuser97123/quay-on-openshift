= What are the healthcheck scripts?

The healthcheck scripts are designed for engagements where a list of
"check items" are evaluated and given a recommendation and a
remediation.

These scripts should be generic enough to use with any technology.
The first usage of these is for an OpenShift 4 Architecture
Review/Healthcheck.

= How do I use these scripts?

Usage is:

```
$ ./scripts/generate-healthcheck.py
----USAGE----
./scripts/generate-healthcheck.py <input directory> <output file>
```

Input directory is a directory which contains an assortment of item
and config files.  Normally, this is in
`<CER_ROOT>/content/healthcheck-items/`.

Output File is the output Asciidoctor file.  The healthcheck script
will overwrite any existing contents of that file, so it is important
not to keep the output in its own separate file, and include it in
main document via includes.

An example run may look like this:
```
cd <CER_ROOT>
./scripts/generate-healthcheck.py ./content/healthcheck-items/ ./content/190_healthcheck-body.adoc 
git commit -m "Updated healtcheck" ./content/190_healthcheck-body.adoc 
./generate_pdf
```

Note:  190_healthcheck-body.adoc number may change based on how many sections are added to CER.

= Are these scripts integrated into the CER CI/CD?

At the moment, no.  The scripts should be run, and then, the output CHECKED INTO GIT.

Since the output of this script is just ASCIIDOC, the CI/CD will pick it up automatically

= What is contained in the input directory?

The input directory contains the following files:

1.  `config.yaml` - (Optional) a file which overrides the default
    configuration for result names, coloring, et cetera.

2.  `categories.yaml` - (Required) a file contains the defined
    categories for the items

3.  `*.item` - (Required) item files contain line items for the health
    check.  There may be many items.

= What is the format for item files?

Item files are individual YAML files with a specific format.

An example:

```
---
version: v0 
metadata:
  category_key: "ocp_config"
  item_evaluated: "Master Nodes are Set"
  product_version: "3+"
  references:  
    - title: "OpenShift Docs"
      url: "https://docs.openshift.com"
    - title: "Red Hat Docs"
      url: "https://docs.redhat.com"
  acceptance_criteria:
    no_change:
      - "Master node number >= 3 and colocated etcd"
      - "Master node number >= 2 and external etcd"
    required:
      - "Master node number < 3 and colocated etcd"
    recommended:
      - "Master node number < 2 and external etcd"
results:
  result_text: "1 master node and colocated etcd"
  recommendation: required
  impact_risk_text: "No High Availability"
  remediation_text: "Redeploy cluster with more nodes"
  additional_comments_text: |-
    BLAH BLAH BLAH
```

This file has major sections:  `metadata` and `results`.

`metadata` contains keys that define the item to be evaluated.  These
will stay consistent between different engagements, and should not be
modified per client.

* `category_key` - The category the item is under.  This key must exist in `categories.yaml`
* `item_evaluated` - A brief description of the item being evaluated.  
* `product_version` - A text description of what version of the product this item applies do.
* `references` - An array of  reference URL/titles for this item.  Generally, a URL to an
  official documentation source describing why this item is important
  and what the proper values should be.
* `acceptance_criteria` - a dictionary of recommendation status keys
  and what a customer environment should look like to meet that
  status.

`results` contains keys with information discovered in the client's
environment.  These will be specific to a specific customer and should
be changed.

* `result_text` - A brief description of what is found by the consultant in the Customer's environment
* `recommendation` - a recommendation status key informing the customer what they should do in response to the `result`.  See "What are the default recommendation status keys?" for more information.
* `impact_risk_text` - What is the impact of this risk, specific to the customer.
* `remediation_text` - What should be done by the customer to remediate this
* `additional_comments_text` - Any additional comments that the consultant wishes to include.

`result_text` is used in tables in the generated Asciidoc.  Thus, should be kept as short as possible.

`impact_risk_text`, `remediation_text`, and `additional_comments_text`
are presented in a detail section below the tables.  Consultants
should be as descriptive as necessary here and can include Asciidoc
syntax.  For long values, consultants should consider using
[https://yaml-multiline.info/](YAML Multiline) syntax.

= What are the default recommendation status keys?

|===
|changes_required|Indicates Changes Required for system stability, subscription compliance, or other reason.
|changes_recommended|Indicates Changes Recommended to align with recommended practices
|advisory|No change required or recommended, but additional information provided.
|na|Not applicable to customer's environment
|no_change|No Change Required.  Environment is in-line with required and recommended practices
|tbe|To Be Evaluated.  Used when delivering draft versions, before the engagement is complete
|===

Each key has built in text and coloring that the script takes care of
automatically.

= What are the rules for an item being printed in the detail section?

If an item has a status of `na`, `tbe` or `no_change` it will not get
printed in the detail section, since there is generally nothing to
say.

If an item with one of these result statuses has the
`additional_comments_text` completed (i.e. is not an empty string),
then a detail section WILL be created, but will exclude the
`impact_risk_text` and `remediation_text` section, REGARDLESS of
whether or not those keys have values in the item's yaml file.
