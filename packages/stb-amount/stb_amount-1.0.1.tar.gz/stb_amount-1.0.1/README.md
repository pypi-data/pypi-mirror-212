# Usage
    sf = SFCalculator(10)
    sf.insert(1)
    print("insert: {}".format(sf.get()))
    sf.update_insert(1, 2)
    print("update insert: {}".format(sf.get()))
    sf.update_remove(1, 2)
    print("update remove: {}".format(sf.get()))
    sf.remove(1)
    print("remove: {}".format(sf.get()))
 
