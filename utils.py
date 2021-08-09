def make_sorted_str(collection):
	if len(collection) == 0: return ""

	sorted_collection = list(collection)
	sorted_collection.sort()
	sorted_str = "% s" % (sorted_collection[0])
	for element in sorted_collection[1:]: sorted_str += ", % s" % (element)
	return sorted_str