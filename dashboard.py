from flask import Blueprint, render_template_string
import csv

<!DOCTYPE html>
<html>
<head>
    <title>Jarvis Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0f0f0f;
            color: #00ffcc;
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #00ffff;
        }
        table {
            width: 90%;
            margin: 20px auto;
            border-collapse: collapse;
            background-color: #1e1e1e;
        }
        th, td {
            padding: 10px;
            border: 1px solid #00ffcc;
        }
        th {
            background-color: #111111;
        }
    </style>
</head>
<body>
    <h1>🚀 Jarvis AI Trade Tracker</h1>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>Pair</th>
            <th>Action</th>
            <th>Result</th>
            <th>Profit</th>
        </tr>
        {% for trade in trades %}
        <tr>
            <td>{{ trade.timestamp }}</td>
            <td>{{ trade.pair }}</td>
            <td>{{ trade.action }}</td>
            <td>{{ trade.result }}</td>
            <td>{{ trade.profit }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
