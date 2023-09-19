import os
def getHTML(list, filepath):
    html = '' 
    temp = '<tr>'
    count = 1
    for stock in list:

        temp += f'<td><img src="charts/{filepath}/{stock}.png"</td>'
        if count % 4 == 0:
            temp += '</tr>'
            html += temp
            temp = '<tr>'
        count += 1
    if temp != "<tr>":
        temp += '</tr>'
        html += temp
    return html

def generateWebPage(bigList, tohList, counts):
    bigDailyHTML = getHTML(bigList,'big-daily')
    bigWeeklyHTML = getHTML(bigList,'big-weekly')
    tohDailyHTML = getHTML(tohList,'toh-daily')
    tohWeeklyHTML = getHTML(tohList,'toh-weekly')

    big_count = counts[0]
    toh_count = counts[1]
    big_filtered_count = counts[2]
    toh_filtered_count = counts[3]

    with open('webpage/resultsOutput.txt', 'w') as f:
        stringToWrite = f"<td colspan=2>Original count: {big_count}</td><td colspan=2>Original count: {toh_count}</td>,"
        stringToWrite += f"<td colspan=2>Filtered count: {big_filtered_count}</td><td colspan=2>Filtered count: {toh_filtered_count}</td>,"
        stringToWrite += bigDailyHTML + ','
        stringToWrite += bigWeeklyHTML + ','
        stringToWrite += tohDailyHTML + ','
        stringToWrite += tohWeeklyHTML
        f.write(stringToWrite)