from columnBuckling import colSafetyMargin, criticalColBuckling, stringerStress

safety_margin=5
span_loc=0 
ribs=[0]

while span_loc<10.8:
    while safety_margin>1:
        span_loc+=0.01
        safety_margin=colSafetyMargin(ribs[-1],span_loc)
        if round(span_loc,3) in [3.8,2.84,10.91] or span_loc>10.9:
            break
    ribs+=[round(span_loc,3)]
    safety_margin=1.1
    
print(ribs)
print(len(ribs))
