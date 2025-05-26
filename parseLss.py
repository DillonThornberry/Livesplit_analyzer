import xml.etree.ElementTree as ET
import pandas as pd
import sys


def main():

    if len(sys.argv) < 3:
        print("Usage: python parseLss.py <lss_file> <optional: folder>")
        sys.exit(1)

    folder = None
    if len(sys.argv) == 3:
        folder = sys.argv[2]
    # Parse the XML file
    tree = ET.parse(f"./lss/{folder + '/' if folder else '' }{sys.argv[1]}")  # Replace with your actual file path
    root = tree.getroot()

    attempts = root.findall('.//AttemptHistory/Attempt')
    segments = root.findall('.//Segments/Segment')

    attemptList = []

    for attempt in attempts:
        attDict = {}
        attDict['id'] = attempt.get('id')
        attDict['started'] = attempt.get('started')
        attDict['ended'] = attempt.get('ended')
        #attDict['realTime'] = attempt.get('RealTime') if attempt.get('RealTime') else None

        # Get nested RealTime
        realTime = attempt.find('RealTime')
        if realTime is not None:
            attDict['realTime'] = realTime.text
        else:
            attDict['realTime'] = None

        attemptList.append(attDict)


    df = pd.DataFrame(attemptList)
    df.set_index('id', inplace=True)

    df['started'] = pd.to_datetime(df['started'], format='%m/%d/%Y %H:%M:%S')
    df['ended'] = pd.to_datetime(df['ended'], format='%m/%d/%Y %H:%M:%S')
    # apeDf['ended'] = pd.to_datetime(apeDf['ended'], format='%Y-%m-%dT%H:%M:%S.%fZ')
    # apeDf['realTime'] = pd.to_timedelta(apeDf['realTime'])

    for segment in segments:
        name = segment.find('Name').text
        
        print(name)
        df[name] = None

        for segmentAttempt in segment.find('SegmentHistory').findall('Time'):
            attId = segmentAttempt.get('id')
            realTime = segmentAttempt.find('RealTime').text if segmentAttempt.find('RealTime') != None else None

            df.at[attId, name] = realTime


    print(df.head())
    
    df.to_csv(f"./csv/{folder + '/' if folder else ''}{sys.argv[1].split('.')[0]}.csv", index=True)
    print(f"Data saved to {sys.argv[1].split('.')[0]}.csv")


if __name__ == "__main__":  
    main()