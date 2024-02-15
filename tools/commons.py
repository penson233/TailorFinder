from config import emailaccount,emailtarget,emailpassword,mailhost
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
#读取文件
def readdomain(filepath):
    with open(filepath,'r') as f:
        read = f.readlines()
    return read


def sendemail(content):
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'html'))
    # 配置调用邮件信息
    msg['Subject'] = 'TailorFinder收集结果'  # 设置邮件主题
    msg['From'] = "TailorFinder"  # 设置发件人


    s = smtplib.SMTP_SSL(mailhost, 465)
    s.login(emailaccount, emailpassword)
    for i in emailtarget:
        msg['To'] = i  # 设置收件人
        s.sendmail(emailaccount, i, msg.as_string())

pre_html='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>台州银行收集结果</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>

    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }

        h1 {
            text-align: center;
            color: #333;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: #fff;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center; /* Center-align the content */
        }

        th {
            background-color: #f2f2f2;
        }

        .filter-input {
            width: 80%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

<h1>TailorFinder收集结果</h1>

<table id="json-table">
    <thead>
        <tr>
            <th>Domain <input type="text" class="filter-input" placeholder="Filter"></th>
            <th>IP <input type="text" class="filter-input" placeholder="Filter"></th>
            <th>Port <input type="text" class="filter-input" placeholder="Filter"></th>
            <th>Server <input type="text" class="filter-input" placeholder="Filter"></th>
            <th>Title <input type="text" class="filter-input" placeholder="Filter"></th>
            <th>Code <input type="text" class="filter-input" placeholder="Filter"></th>
            <th>finger <input type="text" class="filter-input" placeholder="Filter"></th>
        </tr>
    </thead>
    <tbody></tbody>
</table>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
<script>'''

aft_html=''';var tableBody = document.getElementById('json-table').getElementsByTagName('tbody')[0];

    // Populate the table
    jsonData.forEach(function (item) {
        for (var domain in item) {
            var row = tableBody.insertRow();
            var cellDomain = row.insertCell(0);
            var cellIP = row.insertCell(1);
            var cellPort = row.insertCell(2);
            var cellServer = row.insertCell(3);
            var cellTitle = row.insertCell(4);
            var cellCode = row.insertCell(5);
            var fingerText = row.insertCell(6);

            cellDomain.textContent = domain;
            cellIP.textContent = item[domain].ip;
            cellPort.textContent = item[domain].port;
            cellServer.textContent = item[domain].server;
            cellTitle.textContent = item[domain].title;
            cellCode.textContent = item[domain].code;
            fingerText.textContent = item[domain].finger
        }
    });

    // Activate DataTables after the table is fully loaded
    $(document).ready(function () {
        var dataTable = $('#json-table').DataTable();

        // Add search functionality to each column
        $('.filter-input').on('input', function () {
            var columnIndex = $(this).closest('th').index();
            dataTable.column(columnIndex).search(this.value).draw();
        });

        // Add copy button for each column
        $('#json-table thead th').each(function (index) {
            var copyButton = document.createElement('button');
            copyButton.className = 'copy-column-btn';
            copyButton.textContent = 'Copy Column';
            copyButton.setAttribute('data-column-index', index);
            this.appendChild(copyButton);

            var clipboard = new ClipboardJS(copyButton, {
                text: function (trigger) {
                    var columnIndex = trigger.getAttribute('data-column-index');
                    return dataTable.column(columnIndex).data().toArray().join('');
                }
            });

            clipboard.on('success', function (e) {
                alert('Column copied to clipboard!');
            });

            clipboard.on('error', function (e) {
                alert('Copy failed. Please try again.');
            });
        });
    });
</script>

</body>
</html>'''
