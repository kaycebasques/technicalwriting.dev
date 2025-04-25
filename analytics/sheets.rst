.. _sheets:

======================================================
Export Google Analytics data to Sheets via Apps Script
======================================================

.. _Google Apps Script: https://developers.google.com/apps-script
.. _Google Analytics: https://developers.google.com/analytics
.. _Google Sheets: https://workspace.google.com/products/sheets/

This tutorial shows you how to use `Google Apps Script`_ to export your `Google
Analytics`_ data to `Google Sheets`_. The data automatically updates every
night. There's also a custom menu item within Sheets to update the data
on-demand. You can also optionally also expose the data over HTTPS to the public
internet.

.. figure:: /_static/sheets.png

   At the end of the tutorial, you'll get a sheet like this. (All values in this example
   screenshot have been obfuscated or altered.) Explanation of each column:
   
   * **Path** is the docs page. Clicking one of these cells opens that docs page.

   * **Views (One Year)** is how many pageviews the page got in the last 365 days.

   * **Views (Last Month)** is the last 30 days. E.g. if today is September 30th,
     this column tells you all the pageviews between September 1st and September 30th.

   * **Views (Prev. Month)** is the previous 30 days. E.g. if today is September 30th,
     this column tells you all the pageviews between August 2nd and August 31st.

   * **Views Delta (MoM)** shows the month-over-month change in pageviews.
   
   * Average session duration and bounce rate are also provided, but those have been
     cropped out of the screenshot.

.. https://docs.google.com/spreadsheets/d/1Gw8xjbGt728OjAZvd4HTZUgeA0rGYNBcoqdcgH2DvmI/edit?usp=sharing
.. https://script.google.com/macros/s/AKfycbwGWYR08cI78BhMq_5QWiOnaMMkU-q848PMiekSJ1K12RSWmrzkNAzCeHPuK9TWs5A-rw/exec

-------------
Prerequisites
-------------

I assume that you're familiar with Google Sheets and JavaScript programming.

-----
Setup
-----

#. Create a Google Sheets spreadsheet.

   You can name the spreadsheet whatever you want.

#. From the Sheets UI, click **Extensions**  and then click **Apps Script**.

   An Apps Script project will be created and automatically associated to
   the spreadsheet.

   You can name the Apps Script whatever you want. I usually use the exact same name
   of the sheet that the script is connected to.

--------------------------------------
Configure dependencies and permissions
--------------------------------------

On the lefthand side of your Apps Script project (assuming you're using a
left-to-right language like English), there's a list of icons. If you hover
over the top icon a menu expands, and that first icon is called **Overview**. I
will call this list of icons **Project Control**.

#. Hover over **Project Control** and then click **Project Settings**.

#. Enable the **Show "appsscript.json" manifest file in editor** checkbox.

#. Hover over **Project Control** and click **Editor**.

#. Open the **appsscript.json** file.

#. Update the ``dependencies`` to include the official Google Analytics
   library and add an ``oauthScopes`` field to specify the permissions
   that your script needs:

   .. code-block:: json
      :emphasize-lines: 3-11,14-18

      {
        "timeZone": "America/Los_Angeles",
        "dependencies": {
          "enabledAdvancedServices": [
            {
              "userSymbol": "AnalyticsData",
              "version": "v1beta",
              "serviceId": "analyticsdata"
            }
          ]
        },
        "exceptionLogging": "STACKDRIVER",
        "runtimeVersion": "V8",
        "oauthScopes": [
          "https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/script.external_request",
          "https://www.googleapis.com/auth/analytics.readonly"
        ]
      }

   * ``analyticsdata`` gives your script access to the Google Analytics library.
     It's exposed in your script as ``AnalyticsData``.

   * ``https://www.googleapis.com/auth/spreadsheets`` unfortunately gives the
     script access to all your spreadhsheets, which I hate. Why can't I just
     specify that the script should only have access this one sheet with this
     exact ID?? There's a
     ``https://www.googleapis.com/auth/spreadsheets.currentonly`` option that may
     work if you don't need the :ref:`sheets-https` feature.

   * ``https://www.googleapis.com/auth/script.external_request`` can be deleted
     if you're not using the sitemap feature (explained in the comments of ``Code.gs``).

   * ``https://www.googleapis.com/auth/analytics.readonly`` is what enables your
     script to access your analytics data.

-----------------
Create the script
-----------------

#. Open ``Code.gs``.

#. Delete all of the existing code from ``Code.gs``.

#. Copy-paste the following code into ``Code.gs``. Make sure to fix all the TODOs!

   .. code-block:: js

      // Copyright 2025 The Pigweed Authors
      //
      // Licensed under the Apache License, Version 2.0 (the "License"); you may not
      // use this file except in compliance with the License. You may obtain a copy of
      // the License at
      //
      //     https://www.apache.org/licenses/LICENSE-2.0
      //
      // Unless required by applicable law or agreed to in writing, software
      // distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      // WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      // License for the specific language governing permissions and limitations under
      // the License.

      // TODO: Replace `TODO` with your real Google Analytics property ID.
      //
      // To find your property ID, click the **Admin** button at the bottom-left
      // of the Google Analytics website (assuming you're using a left-to-right
      // language like English), then expand the **Property** section, then click
      // **Property details**.
      const PROPERTY_ID = 'properties/TODO';
      // TODO: Replace `TODO` with your real Google Sheets ID.
      // It's the part after `https://docs.google.com/spreadsheets/d/`
      // and before `/edit`. Example:
      // https://docs.google.com/spreadsheets/d/THIS_PART_IS_YOUR_SHEET_ID/edit
      const SHEET_ID = 'TODO';
      // TODO: Replace `TODO` with the name of the sheet where the data
      // will be populated. If you didn't modify the default sheet name,
      // then the value here should be `Sheet1`.
      const SHEET_NAME = 'TODO';
      // TODO: Replace `TODO` with your real domain, e.g. `https://example.com`.
      // Omit the trailing slash.
      const DOMAIN = 'TODO';
      // TODO: Uncomment the next line and replace `TODO` with the path to
      // your sitemap if you're using the sitemap filtering feature.
      // const SITEMAP = `${DOMAIN}TODO`;

      // Retrieve all the analytics data through a single request. Efficient!
      function initRequest(start, end) {
        const request = AnalyticsData.newRunReportRequest();
        // https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#metrics
        request.metrics = [];
        const metrics = [
          'screenPageViews',
          'averageSessionDuration',  // Provided in seconds.
          'bounceRate',  // Provided as a float between 0.0 and 1.0, where 1.0 means 100% of users bounced.
        ];
        metrics.forEach(m => {
          let metric = AnalyticsData.newMetric();
          metric.name = m;
          request.metrics.push(metric);
        })
        // https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema#dimensions
        request.dimensions = [];
        const dimensions = [
          'pagePath',
        ];
        dimensions.forEach(d => {
          let dimension = AnalyticsData.newDimension();
          dimension.name = d;
          request.dimensions.push(dimension);
        });
        request.dateRanges = [];
        const dateRanges = [
          ['365daysAgo', 'today', 'LAST_365_DAYS'],
          ['30daysAgo', 'today', 'LAST_30_DAYS'],
          ['60daysAgo', '30daysAgo', 'PREV_30_DAYS'],
        ];
        dateRanges.forEach(dr => {
          let dateRange = AnalyticsData.newDateRange();
          dateRange.startDate = dr[0];
          dateRange.endDate = dr[1];
          dateRange.name = dr[2];
          request.dateRanges.push(dateRange);
        });
        return request;
      }

      function runReport() {
        const request = initRequest();
        const report = AnalyticsData.Properties.runReport(request, PROPERTY_ID);
        // Logger.log(report);
        //
        // The report data is structured like this:
        //
        // {
        //   "rows": [
        //     {
        //       "metricValues": [100, 30.0, 0.1],
        //       "dimensionValues": ["index.html", "LAST_365_DAYS"],
        //     },
        //     {
        //       "metricValues": [62, 90.0, 0.6],
        //       "dimensionValues": ["overview.html", "LAST_30_DAYS"],
        //     },
        //   ]
        // }
        //
        // The metrics are presented in the order that `initRequest()` specifies. I.e.
        // the first value is pageviews, the second is average session duration,
        // and the third is bounce rate.
        //
        // First dimension value is the page path, second value is the timeframe ID.
        return report;
      }

      // TODO: Uncomment this if you want to filter out URLs that aren't specified in your
      // sitemap. If your site uses redirection of any sort then this is probably going to be
      // too strict and will incorrectly filter out valid URLs that get redirected.
      // function getSitemap() {
      //   const response = UrlFetchApp.fetch(SITEMAP);
      //   if (response.getResponseCode() !== 200) {
      //     return null;
      //   } else {
      //     const content = response.getContentText();
      //     const document = XmlService.parse(content);
      //     const root = document.getRootElement();
      //     const ns = root.getNamespace(); // Get the default namespace if it exists
      //     const nodes = root.getChildren('url', ns); // Assuming standard sitemap format
      //     let urls = [];
      //     nodes.forEach(node => {
      //       const loc = node.getChild('loc', ns);
      //       urls.push(loc.getText());
      //     });
      //     return urls;
      //   }
      // }

      // Rearrange the report data as an object where the top-level keys are
      // page paths and all of the data for that page can be accessed under its
      // key, like this:
      //
      // {
      //   "/index.html": {
      //     "pageviews_LAST_365_DAYS": 100,
      //     "pageviews_LAST_30_DAYS": 25,
      //     "pageviews_PREV_30_DAYS": 35,
      //     "session_LAST_365_DAYS": 100,
      //     "session_LAST_30_DAYS": 93,
      //     "session_PREV_30_DAYS": 89,
      //     "bounce_LAST_365_DAYS": 0.4,
      //     "bounce_LAST_30_DAYS": 0.6,
      //     "bounce_PREV_30_DAYS": 0.3,
      //   },
      //   …
      // }
      //
      // If you're using the sitemap filtering feature, this function also is
      // where the filtering happens.
      function normalize(report) {
        let data = {};
        // TODO: Uncomment this if you're using the sitemap filtering feature.
        // const sitemap = getSitemap();
        for (const i in report.rows) {
          const row = report.rows[i];
          const path = row.dimensionValues[0].value;
          const url = `${DOMAIN}${path}`;
          // TODO: Uncomment this if you're using the sitemap filtering feature.
          // if (!sitemap.includes(url)) {
          //   Logger.log(`WARNING: Ignoring ${url}`);
          //   continue;
          // }
          const pageviews = row.metricValues[0].value;
          const session = row.metricValues[1].value;
          // By default the bounce rate is a value between 0.0 and 1.0, where
          // 1.0 indicates that 100% of users bounced. Convert it to a number
          // between 0 and 100 to make it easier to compute the delta later.
          const bounce = row.metricValues[2].value * 100;
          const timeframe = row.dimensionValues[1].value;
          if (!(path in data)) {
            data[path] = {};
          }
          data[path][`pageviews_${timeframe}`] = pageviews;
          data[path][`session_${timeframe}`] = session;
          data[path][`bounce_${timeframe}`] = bounce;
        }
        return data;
      }

      function calculateDelta(last, prev) {
        if (last == 0) {
          return 'N/A';
        } else if (prev == 0) {
          return 'N/A';
        } else {
          return Math.floor(((last / prev) - 1) * 100);
        }
      }

      // Prepare all of the spreadsheet cell data so that we can update the
      // sheet in one fell swoop.
      function toCells(data) {
        cells = [[
          'Path',
          `Views (One Year)`,
          `Views (Last Month)`,
          `Views (Prev. Month)`,
          `Views Delta (MoM)`,
          `Session (One Year)`,
          `Session (Last Month)`,
          `Session (Prev. Month)`,
          `Session Delta (MoM)`,
          `Bounce (One Year)`,
          `Bounce (Last Month)`,
          `Bounce (Prev. Month)`,
          `Bounce Delta (MoM)`,
        ]];
        for (const path in data) {
          const page = data[path];
          cells.push([
            `=HYPERLINK("${DOMAIN}${path}", "${path}")`,
            // Pageviews are supposed to be ints 
            Math.floor(page['pageviews_LAST_365_DAYS']),
            Math.floor(page['pageviews_LAST_30_DAYS']),
            Math.floor(page['pageviews_PREV_30_DAYS']),
            calculateDelta(page['pageviews_LAST_30_DAYS'], page['pageviews_PREV_30_DAYS']),
            // The session duration and bounce rate numbers are provided as floats.
            // We don't need that much detail. It makes the sheet too noisy.
            Math.floor(page['session_LAST_365_DAYS']),
            Math.floor(page['session_LAST_30_DAYS']),
            Math.floor(page['session_PREV_30_DAYS']),
            calculateDelta(page['session_LAST_30_DAYS'], page['session_PREV_30_DAYS']),
            Math.floor(page['bounce_LAST_365_DAYS']),
            Math.floor(page['bounce_LAST_30_DAYS']),
            Math.floor(page['bounce_PREV_30_DAYS']),
            calculateDelta(page['bounce_LAST_30_DAYS'], page['bounce_PREV_30_DAYS']),
          ]);
        }
        return cells;
      }

      // Delete all previous data from the sheet and insert the new data.
      function updateSheet(cells) {
        const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
        const sheet = spreadsheet.getSheetByName(SHEET_NAME);
        sheet.getRange('A1:Z1000').clearContent();
        const columnMap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        // Infer how many columns we need by looking at the length of the provided cells data.
        const lastColumn = columnMap[cells[0].length - 1];
        const a1 = `A1:${lastColumn}${cells.length}`;
        const range = sheet.getRange(a1);
        range.setValues(cells);
      }

      // Color the delta columns dark red, light red, light green, or dark green.
      function formatDeltaColumns() {
        const DARK_RED = '#FF4D4D';
        const LIGHT_RED = '#FFD9D9';
        const DARK_GREEN = '#4ea96b';
        const LIGHT_GREEN = '#e2f0e6';
        const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
        const sheet = spreadsheet.getSheetByName(SHEET_NAME);
        // Delete previous rules.
        sheet.setConditionalFormatRules([]);
        const viewsDelta = sheet.getRange('E1:E');
        const sessionDelta = sheet.getRange('I1:I');
        const bounceDelta = sheet.getRange('M1:M');
        var rules = sheet.getConditionalFormatRules();
        var majorDecrease = SpreadsheetApp.newConditionalFormatRule()
            .whenNumberLessThan(-50)
            .setBackground(DARK_RED)
            .setRanges([viewsDelta, sessionDelta, bounceDelta])
            .build();
        rules.push(majorDecrease);
        var minorDecrease = SpreadsheetApp.newConditionalFormatRule()
            .whenNumberBetween(-50, 0)
            .setBackground(LIGHT_RED)
            .setRanges([viewsDelta, sessionDelta, bounceDelta])
            .build();
        rules.push(minorDecrease);
        var minorIncrease = SpreadsheetApp.newConditionalFormatRule()
            .whenNumberBetween(0, 50)
            .setBackground(LIGHT_GREEN)
            .setRanges([viewsDelta, sessionDelta, bounceDelta])
            .build();
        rules.push(minorIncrease);
        var majorIncrease = SpreadsheetApp.newConditionalFormatRule()
            .whenNumberGreaterThan(50)
            .setBackground(DARK_GREEN)
            .setRanges([viewsDelta, sessionDelta, bounceDelta])
            .build();
        rules.push(majorIncrease);
        sheet.setConditionalFormatRules(rules);
      }

      function main() {
        const report = runReport();
        const data = normalize(report);
        const cells = toCells(data);
        updateSheet(cells);
        formatDeltaColumns();
        return data;
      }

      // Add a menu item to the Google Sheets UI that lets users update
      // the analytics data on-demand.
      function onOpen() {
        SpreadsheetApp.getUi()
            .createMenu('Analytics')
            .addItem('Update', 'main')
            .addToUi();
      }

      // Publicly expose the data as JSON over a web service.
      // This requires some extra setup via the Apps Script UI.
      function doGet(e) {
        const data = JSON.stringify(main());
        return ContentService.createTextOutput(data).setMimeType(ContentService.MimeType.JSON);
      }

#. Did you remember to fix all the TODOs in ``Code.gs``???

-----------------
Grant permissions
-----------------

Run the script manually so that you can explicitly approve the
permissions that are requested in ``appsscript.json``.

#. Between **Debug** and **Execution log** there is a dropdown.
   Click that dropdown and select **main**.

#. Click **Run**.

#. Click **Review permissions**. An OAuth popup appears.

#. In the popup, give the script access to the permissions
   that it's requesting.

-------------------------------------
Automatically update the data nightly
-------------------------------------

#. Hover over **Project Control** and click **Triggers**.

#. Click **Add Trigger**.

#. For **Choose which function to run** select **main**.

#. For **Choose which deployment should run** select **Head**.

#. For **Select event source** select **Time-driven**.

#. For **Select type of time based trigger** select **Day timer**.

#. For **Select time of day** select **Midnight to 1am**.

#. For **Failure notification settings** select **Notify me immediately**.

#. Click **Save**.

.. _sheets-https:

-----------------------------------
Publicly expose the data over HTTPS
-----------------------------------

You should never do this on your employer's sites without
written approval (and a business need). In the future I'm going
to expose the analytics for ``technicalwriting.dev`` so that I can
generate a "top 10 most popular blog posts" page.

#. From any Apps Script page, click **Deploy** and then select **New deployment**.

#. Click the gear icon next to **Select type** and select **Web app**.

#. For **Description** enter any name you want.

#. For **Execute as** select **Me**.

#. For **Who has access** select **Anyone**.

#. Click **Deploy**.

#. Copy the **Web app** URL.

#. Paste the web app URL into a browser and verify that the analytics data
   is sent as JSON.

