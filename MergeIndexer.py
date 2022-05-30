class MergeIndexer:
  def __init__(self, num_files: int = 0):
    self.num_files = num_files
    self.finaldisknum = 1

  def merge_all_indexers(self):
    # JAEDYN'S CODE
    # Merge 1: Disk1 + Disk2 = Final1
    # Merge 2: Final1 + Disk3 = Final2
    # Merge 3: Final2 + Disk4 = Final3 (final!)
    
    self.merge_two_disks("disk1.txt", "disk2.txt")
    merge_count = 1
    disk_num = 3

    while disk_num <= self.num_files:
      first_file = "mergedDisk" + str(merge_count) + ".txt"
      second_file = "disk" + str(disk_num) + ".txt"

      self.merge_two_disks(first_file, second_file)
      merge_count += 1
      disk_num += 1

    return "mergedDisk" + str(merge_count) + ".txt" # should be the final disk's name


  # takes in path to disk1 and path to disk2, merge both
  # of them and returns a new file containing the merged disks
  def merge_two_disks(self, disk1: str, disk2: str) -> str:

    f1 = open(disk1, "r")
    f2 = open(disk2, "r")

    # TODO: used to reset position in the files
    f1.seek(0)
    f2.seek(0)

    # read the first line in disk1 and disk2 (do this only once, edge case...)
    current_line_f1 = next(f1)
    current_line_f2 = next(f2)
    
    # create chunks from disk1 and disk2 via alphabet letters
    for letter in "abcdefghijklmnopqrstuvwxyz":
      
      lines_in_f1 = []
      lines_in_f2 = []
      
      # read from disk1
      try:
          while current_line_f1.startswith('"' + letter):             
              lines_in_f1.append(current_line_f1)
              current_line_f1 = next(f1)

      except StopIteration as e:
          # print("StopIteration for disk1")
          pass

      # read from disk2
      try:
          while current_line_f2.startswith('"' + letter):
              lines_in_f2.append(current_line_f2)
              current_line_f2 = next(f2)

      except StopIteration as e:
          # print("StopIteration for disk2")
          pass

      # TODO: to be deleted
      # print('lines_in_f1: ', lines_in_f1)
      # print('lines_in_f2: ', lines_in_f2)

      # merge lines_in_f1 + lines_in_f2
      merged_chunks_list = self.merge_two_disk_chunks(lines_in_f1, lines_in_f2)
      
      # write the merged postings for a single letter into final file
      finaldiskname = "mergedDisk" + str(self.finaldisknum) + ".txt"
      with open("mergedDisk" + str(self.finaldisknum) + ".txt", "a") as f:
        for serialized_index in merged_chunks_list:      
          f.write(serialized_index)
    
    self.finaldisknum += 1
    
    f1.close()
    f2.close()

    return finaldiskname


  # takes in two lists and returns a merged list 
  def merge_two_disk_chunks(self, postings1: list, postings2: list) -> list:
    merged_chunks_list = []
    p1, p2 = 0, 0

    while p1 < len(postings1) and p2 < len(postings2):

      first_line = postings1[p1] 
      second_line = postings2[p2]

      
      first_token, second_token = first_line.split(":")[0], second_line.split(":")[0]
      

      if first_token != second_token:
        if first_token < second_token:
          merged_chunks_list.append(first_line) 
          p1 += 1
        else:
          merged_chunks_list.append(second_line)
          p2 += 1

      else:
        merged_postings_string = self.merge_two_postings(first_line, second_line)
                
        merged_chunks_list.append(merged_postings_string)
        p1 += 1
        p2 += 1
      
    # do this after the exhausting both lists from above
    while p1 < len(postings1):
      merged_chunks_list.append(postings1[p1])
      p1 += 1

    while p2 < len(postings2):
      merged_chunks_list.append(postings2[p2])
      p2 += 1

    return merged_chunks_list # return ["begin:|1,2|4,7|8,10|", "fish:|3,8|", "hello:|2,2|8,6|"]
  

  # given two lines (each line is from a different file), 
  # returns a string containing postings from both lines
  # first_line = "begin: |1,2|"       => ["begin", "|1,2|""]
  # second_line = "begin: |4,7|8,10|" => ["begin", "|4,7|8,10|"]
  def merge_two_postings(self, first_line: str, second_line: str) -> str:
    first_line_postings = first_line.split(':')[1].rstrip('"\n')             # "|1,2|"
    second_line_postings = second_line.split(':')[1][1:]                    # "|4,7|8,10|"] => "4,7|8,10|"
    merged_postings = first_line_postings + second_line_postings            # "|1,2|4,7|8,10|"

    return first_line.split(':')[0] + ":" + merged_postings                 # "begin:|1,2|4,7|8,10|"
    