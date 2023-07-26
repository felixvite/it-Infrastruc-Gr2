def convert_to_block(user_time):
    # Convert user_time to an integer representing total minutes
    hours, minutes = map(int, user_time.split(':'))
    total_minutes = hours * 60 + minutes

    # Define time blocks in the same format as in the database
    time_blocks = ['0000-0559', '0600-0659', '0700-0759', '0800-0859', '0900-0959', '1000-1059', '1100-1159', '1200-1259',
    '1300-1359', '1400-1459', '1500-1559', '1600-1659', '1700-1759', '1800-1859', '1900-1959', '2000-2059', '2100-2159',
    '2200-2259', '2300-2359']

    # Loop through time_blocks to find the block that contains user_time
    for block in time_blocks:
        start, end = block.split('-')
        start_hours, start_minutes = int(start[:2]), int(start[2:])
        end_hours, end_minutes = int(end[:2]), int(end[2:])

        # Convert block start and end times to total minutes
        start_total = start_hours * 60 + start_minutes
        end_total = end_hours * 60 + end_minutes

        # Check if user_time falls within this block
        if start_total <= total_minutes < end_total:
            return block

    # Return None if user_time does not fall within any block
    return None

print(convert_to_block('23:00'))