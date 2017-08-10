class employee():

    def __init__(self,name,last,age):
        self.name=name
        self.last=last
        self.age=age

em1=employee("ankit","satya",21)

print "{} {}".format(em1.name,em1.last)

