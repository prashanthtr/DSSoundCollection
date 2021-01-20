
# returns the longest substring less than cutoff value
# Used to determine whether array is silent
def longSilence(arr,e):
    substrLen = []
    cnt = 0
    for x in arr:
        if abs(x) < e:
            cnt = cnt+1;
        else:
            substrLen.append(cnt)
            cnt=0;
    if len(substrLen)==0:
            substrLen.append(cnt)
    #print("max",max(substrLen))
    return max(substrLen)<=len(arr)/2
