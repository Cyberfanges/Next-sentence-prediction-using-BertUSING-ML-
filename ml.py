def findOverlappingTimes(intervals):
    if not intervals:
        return []

    # Sort the intervals by their start times
    intervals.sort(key=lambda x: x[0])

    merged_intervals = [intervals[0]]
    
    for interval in intervals[1:]:
        current_start, current_end = merged_intervals[-1]
        new_start, new_end = interval
        
        if current_end >= new_start:
            # There is an overlap, merge the intervals
            merged_intervals[-1] = [current_start, max(current_end, new_end)]
        else:
            # No overlap, add the interval to the result
            merged_intervals.append(interval)

    return merged_intervals

if __name__ == '__main__':
    intervals = [[7, 7], [2, 3], [6, 11], [1, 2]]
    result = findOverlappingTimes(intervals)
    print(result)  # Output should be [[1, 3], [6, 11]]
