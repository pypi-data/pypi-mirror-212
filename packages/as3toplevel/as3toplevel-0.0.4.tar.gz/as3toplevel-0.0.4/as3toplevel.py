import math as m
import random as r
from numpy import nan
from numpy import inf
from numpy import NINF
from numpy import base_repr
from textwrap import wrap
from time import time, strftime
from datetime import datetime

def listtoarray(l:list):
   """
   A function to convert a python list to an Array.
   """
   tempArray = Array()
   for i in range(0,len(l)):
      tempArray[i] = l[i]
   return tempArray

def escapeFullConvert(Str):
   """
   Converts the parameter to a string and encodes it in a URL-encoded format, where characters are replaced with % hexadecimal sequences. When used in a URL-encoded string, the percentage symbol (%) is used to introduce escape characters, and is not equivalent to the modulo operator (%). 
   """
   tempdict1 = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '€', '\x81', '‚', 'ƒ', '„', '…', '†', '‡', 'ˆ', '‰', 'Š', '‹', 'Œ', '\x8d', 'Ž', '‘', '\X8f', '\x90', '’', '“', '”', '•', '–', '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '!', '\xa0', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']
   tempdict2 = ['%20', '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29', '%2A', '%2B', '%2C', '%2D', '%2E', '%2F', '%30', '%31', '%32', '%33', '%34', '%35', '%36', '%37', '%38', '%39', '%3A', '%3B', '%3C', '%3D', '%3E', '%3F', '%40', '%41', '$42', '%43', '%44', '%45', '%46', '%47', '%48', '%49', '%4A', '%4B', '%4C', '%4D', '%4E', '%4F', '%50', '%51', '%52', '%53', '%54', '%55', '%56', '%57', '%58', '%59', '%5A', '%5B', '%5C', '%5D', '%5E', '%5F', '%60', '%61', '%62', '%63', '%64', '%65', '%66', '%67', '%68', '%69', '%6A', '%6B', '%6C', '%6D', '%6E', '%6F', '%70', '%71', '%72', '%73', '%74', '%75', '%76', '%77', '%78', '%79', '%7A', '%7B', '%7C', '%7D', '%7E', '%7F', '%80', '%81', '%82', '%83', '%84', '%85', '%86', '%87', '%88', '%89', '%8A', '%8B', '%8C', '%8D', '%8E', '%8f', '%90', '%91', '%92', '%93', '%94', '%95', '%96', '%97', '%98', '%99', '%9A', '%9B', '%9C', '%9D', '%9E', '%9F', '%A0', '%A1', '%A2', '%A3', '%A4', '%A5', '%A6', '%A7', '%A8', '%A9', '%AA', '%AB', '%AC', '%AD', '%AE', '%AF', '%B0', '%B1', '%B2', '%B3', '%B4', '%B5', '%B6', '%B7', '%B8', '%B9', '%BA', '%BB', '%BC', '%BD', '%BE', '%BF', '%C0', '%C1', '%C2', '%C3', '%C4', '%C5', '%C6', '%C7', '%C8', '%C9', '%CA', '%CB', '%CC', '%CD', '%CE', '%CF', '%D0', '%D1', '%D2', '%D3', '%D4', '%D5', '%D6', '%D7', '%D8', '%D9', '%DA', '%DB', '%DC', '%DD', '%DE', '%DF', '%E0', '%E1', '%E2', '%E3', '%E4', '%E5', '%E6', '%E7', '%E8', '%E9', '%EA', '%EB', '%EC', '%ED', '%EE', '%EF', '%F0', '%F1', '%F2', '%F3', '%F4', '%F5', '%F6', '%F7', '%F8', '%F9', '%FA', '%FB', '%FC', '%FD', '%FE', '%FF']
   tempString1 = str(Str)
   templist = wrap(tempString1, 1)
   tempString2 = String()
   for i in range(0,len(templist)):
      try:
         tempi = tempdict1.index(templist[i])
      except:
         tempi = -1
      if tempi == -1:
         tempString2 += ""
      else:
         tempString2 += tempdict2[tempi]
   return tempString2

class NInfinity:
   def __init__(self):
      self.string = "-Infinity"
      self.value = NINF
   def __str__(self):
      return self.string
   def __repr__(self):
      return self.value
class Infinity:
   def __init__(self):
      self.string = "Infinity"
      self.value = inf
   def __str__(self):
      return self.string
   def __repr__(self):
      return self.value
class NaN:
   def __init__(self):
      self.string = "NaN"
      self.value = nan
   def __str__(self):
      return self.string
   def __repr__(self):
      return self.value
class undefined:
   def __init__(self):
      self.value = "undefined"
   def __str__(self):
      return self.value

class ArgumentError(Exception):
   def __init__(self, message=""):
      self.error = message
class Array:
   """
   Lets you create array objects similar to ActionScript3
   Instead of making two different init functions, I made init create an array based on the values passed to it and another method called toSize to make the array a specific size. toSize fills all empty slots with the None object (since python doesn't have a null or undefined type) or deletes excess slots if there are more. WARNING: If nothing is passed to this method and it is called while there is data inside the array, all data in the array will be erased.
   """
   CASEINSENSITIVE = 1
   DESCENDING = 2
   UNIQUESORT = 4
   RETURNINDEXEDARRAY =  8
   NUMERIC = 16
   def __init__(self, *values):
      self.array = []
      for i in range(0,len(values)):
         self.array.append(values[i])
   def __str__(self):
      return f'{self.array}'
   def __len__(self):
      return len(self.array)
   def __getitem__(self, item):
      try:
         if self.array[item] == None:
            return "undefined"
         else:
            return self.array[item]
      except:
         return ""
   def __setitem__(self, item, value):
      if item + 1 > len(self.array):
         self.toSize(item + 1)
      self.array[item] = value
   def toSize(self, numElements=0):
      """
      Instead of making two different init functions, I made init create an array based on the values passed to it and this method to make the array a specific size. This method fills all empty slots with the None object (since python doesn't have a null or undefined type) or deletes excess slots if there are more. WARNING: If nothing is passed to this method and it is called while there is data inside the array, all data in the array will be erased.
      """
      if numElements < 0:
         raise Exception("RangeError")
      elif numElements == 0:
         self.array = []
      elif len(self) > numElements:
         while len(self) > numElements:
            self.pop()
      elif len(self) < numElements:
         while len(self) < numElements:
            self.push(None)
   def length(self):
      return len(self.array)
   def concat(self, *args):
      """
      Concatenates the elements specified in the parameters with the elements in an array and creates a new array. If the parameters specify an array, the elements of that array are concatenated. If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         *args — A value of any data type (such as numbers, elements, or strings) to be concatenated in a new array.
      Returns:
         Array — An array that contains the elements from this array followed by elements from the parameters.
      """
      if len(args) == 0:
         raise Exception("Must have at least 1 arguments")
      else:
         for i in range(0,len(args)):
            if self.array == []:
               self.array = args[i]
            else:
               if type(args[i]) == list or type(args[i]) == tuple or type(args[i]) == Array:
                  b = args[i]
                  c = 0
                  for c in range(0,len(b)):
                     self.push(b[c])
               else:
                  self.push(args[i])
   def every(self, callback):
      """
      Executes a test function on each item in the array until an item is reached that returns False for the specified function. You use this method to determine whether all items in an array meet a criterion, such as having values less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if all items in the array return True for the specified function; otherwise, False.
      """
      tempBool = True
      for i in range(0,len(self)):
         if callback(self[i], i, self) == False:
            tempBool == False
            break
      return tempBool
   def filter(self, callback):
      """
      Executes a test function on each item in the array and constructs a new array for all items that return True for the specified function. If an item returns False, it is not included in the new array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example, item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains all items from the original array that returned True. 
      """
      tempArray = Array()
      for i in range(0,len(self)):
         if callback(self[i], i, self) == True:
            tempArray.push(self[i])
      return tempArray
   def forEach(self, callback):
      """
      Executes a function on each item in the array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (for example, a trace() statement) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      """
      for i in range(0, len(self)):
         self[i] = callback(self[i], i, self)
   def indexOf(self, searchElement, fromIndex=0):
      """
      Searches for an item in an array using == and returns the index position of the item.
      Parameters:
         searchElement — The item to find in the array.
         fromIndex:int (default = 0) — The location in the array from which to start searching for the item.
      Returns:
         index:int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      """
      index = -1
      i = fromIndex
      while i < len(self):
         if self[i] == searchElement:
            index = i
            i = len(self)
         else:
            i += 1
      return index
   def insertAt(self, index, element):
      """
      Insert a single element into an array.
      Parameters
	      index:int — An integer that specifies the position in the array where the element is to be inserted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
	      element — The element to be inserted.
      """
      if index < 0:
         self.array.insert((len(l1) - abs(index)), element)
      else:
         self.array.insert(index, element)
   def join(self, sep=","):
      """
      Converts the elements in an array to strings, inserts the specified separator between the elements, concatenates them, and returns the resulting string. A nested array is always separated by a comma (,), not by the separator passed to the join() method.
      Parameters:
	      sep (default = ",") — A character or string that separates array elements in the returned string. If you omit this parameter, a comma is used as the default separator.
      Returns:
	      String — A string consisting of the elements of an array converted to strings and separated by the specified parameter.
      """
      result = ""
      i = 0
      for i in range(0, len(self)):
         if i != len(self) - 1:
            result += str(self[i]) + str(sep)
         else:
            result += str(self[i])
         i += 1
      return result
   def lastIndexOf(self, searchElement, fromIndex=99*10^99):
      """
      Searches for an item in an array, working backward from the last item, and returns the index position of the matching item using ==.
      Parameters:
	      searchElement — The item to find in the array.
	      fromIndex:int (default = 99*10^99) — The location in the array from which to start searching for the item. The default is the maximum value allowed for an index. If you do not specify fromIndex, the search starts at the last item in the array.
      Returns:
	      int — A zero-based index position of the item in the array. If the searchElement argument is not found, the return value is -1.
      """
      index = -1
      for i in range(0,len(self)):
         l = len(self) - i - 1
         if self[l] == searchElement:
            index = l
            break
      return index
   def map(self, callback):
      """
      Executes a function on each item in an array, and constructs a new array of items corresponding to the results of the function on each item in the original array.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple command (such as changing the case of an array of strings) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Array — A new array that contains the results of the function on each item in the original array.
      """
      output = Array()
      output.toSize(len(self))
      for i in range(0,len(self)):
         output[i] = callback(self[i], i, self)
      return output
   def pop(self):
      """
      Removes the last element from an array and returns the value of that element.
      Returns:
         * — The value of the last element (of any data type) in the specified array.
      """
      i = len(self) - 1
      value = self[i]
      self.array.pop(i)
      return value
   def push(self, *args):
      """
      Adds one or more elements to the end of an array and returns the new length of the array.
      Parameters:
         *args — One or more values to append to the array. 
      """
      i = 0
      while i < len(args):
         self.array.append(args[i])
         i += 1
   def removeAt(self, index):
      """
      Remove a single element from an array. This method modifies the array without making a copy.
      Parameters:
	      index:int — An integer that specifies the index of the element in the array that is to be deleted. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
      Returns:
	      * — The element that was removed from the original array.
      """
      if index >= 0:
         value = self[index]
         self.array.pop(index)
      else:
         i = len(self) - 1 + index
         value = self[i]
         self.array.pop(i)
      return value
   def reverse(self):
      """
      Reverses the array in place.
      Returns:
	      Array — The new array.
      """
      a = Array()
      for i in range(0, len(self)):
         a.array.append(self[len(self) - 1 - i])
      for i in range(0, len(self)):
         self[i] = a[i]
   def shift(self):
      """
      Removes the first element from an array and returns that element. The remaining array elements are moved from their original position, i, to i-1.
      Returns:
         * — The first element (of any data type) in an array. 
      """
      value = self[0]
      for i in range(0,len(self)):
         if i < len(self) - 1:
            self[i] = self[i+1]
         else:
            self.pop()
      return value
   def slice(self, startIndex=0, endIndex=99*10^99):
      """
      Returns a new array that consists of a range of elements from the original array, without modifying the original array. The returned array includes the startIndex element and all elements up to, but not including, the endIndex element.
      If you don't pass any parameters, the new array is a duplicate (shallow clone) of the original array.
      Parameters:
         startIndex:int (default = 0) — A number specifying the index of the starting point for the slice. If startIndex is a negative number, the starting point begins at the end of the array, where -1 is the last element.
         endIndex:int (default = 99*10^99) — A number specifying the index of the ending point for the slice. If you omit this parameter, the slice includes all elements from the starting point to the end of the array. If endIndex is a negative number, the ending point is specified from the end of the array, where -1 is the last element.
      Returns:
         Array — An array that consists of a range of elements from the original array.
      """
      i = startIndex
      result = Array()
      if endIndex > len(self):
         ei = len(self)
      else:
         ei = endIndex
      while i < ei:
         result.push(self[i])
         i += 1
      return result
   def some(self, callback):
      """
      Executes a test function on each item in the array until an item is reached that returns True. Use this method to determine whether any items in an array meet a criterion, such as having a value less than a particular number.
      Parameters:
         callback:Function — The function to run on each item in the array. This function can contain a simple comparison (for example item < 20) or a more complex operation, and is invoked with three arguments; the value of an item, the index of an item, and the Array object:
         - function callback(item:*, index:int, array:Array)
      Returns:
         Boolean — A Boolean value of True if any items in the array return True for the specified function; otherwise False.
      """
      tempBool = False
      for i in range(0,len(self)):
         if callback(self[i], i, self) == Ture:
            tempBool == True
            break
      return tempBool
   def sort(sortOptions=0):
      """
      """
      if sortOptions == 0:
         raise Exception("Not yet implemented")
      elif sortOptions == 1:
         raise Exception("Not yet implemented")
      elif sortOptions == 2:
         raise Exception("Not yet implemented")
      elif sortOptions == 4:
         raise Exception("Not yet implemented")
         pass
      elif sortOptions == 8:
         raise Exception("Not yet implemented")
      elif sortOptions == 16:
         self.array.sort()
   def sortOn():
      pass
   def splice(self, startIndex, deleteCount, *values):
      """
      Adds elements to and removes elements from an array. This method modifies the array without making a copy.
      Parameters:
	      startIndex:int — An integer that specifies the index of the element in the array where the insertion or deletion begins. You can use a negative integer to specify a position relative to the end of the array (for example, -1 is the last element of the array).
	      deleteCount:int — An integer that specifies the number of elements to be deleted. This number includes the element specified in the startIndex parameter. If you do not specify a value for the deleteCount parameter, the method deletes all of the values from the startIndex element to the last element in the array. If the value is 0, no elements are deleted.
	      *values — An optional list of one or more comma-separated values to insert into the array at the position specified in the startIndex parameter. If an inserted value is of type Array, the array is kept intact and inserted as a single element. For example, if you splice an existing array of length three with another array of length three, the resulting array will have only four elements. One of the elements, however, will be an array of length three.
      Returns:
	      Array — An array containing the elements that were removed from the original array. 
      """
      removedValues = Array()
      i = deleteCount
      while i > 0:
         removedValues.push(self[startIndex])
         self.removeAt(startIndex)
         i -= 1
      if len(values) > 0:
         for i in range(0,len(values)):
            self.insertAt(startIndex + i, values[i])
      return removedValues
   def toLocaleString(self):
      """
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. In the ActionScript 3.0 implementation, this method returns the same value as the Array.toString() method.
      Returns:
	      String — A string of array elements. 
      """
      return self.toString()
   def toString(self):
      """
      Returns a string that represents the elements in the specified array. Every element in the array, starting with index 0 and ending with the highest index, is converted to a concatenated string and separated by commas. To specify a custom separator, use the Array.join() method.
      Returns:
	      String — A string of array elements. 
      """
      a = ""
      for i in range(0, len(l1)):
         if i == len(l1) - 1:
            a += str(self[i])
         else:
            a += str(self[i]) + ","
      return a
   def unshift(self, *args):
      """
      Adds one or more elements to the beginning of an array and returns the new length of the array. The other elements in the array are moved from their original position, i, to i+1.
      Parameters:
	      *args — One or more numbers, elements, or variables to be inserted at the beginning of the array.
      Returns:
	      int — An integer representing the new length of the array.
      """
      a = Array()
      for i in range(0, len(args)):
         a.push(args[i])
      for i in range(0, len(self)):
         a.push(self[i])
      for i in range(0, len(self)):
         self[i] = a[i]
      for i in range(len(self), len(a)):
         self.push(a[i])
      return len(self)
class Boolean:
   """
   Lets you create boolean object similar to ActionScript3
   Since python is case sensitive the values are "True" or "False" instead of "true" or "false"
   """
   def __init__(self, expression=False):
      self.bool = self.Boolean(expression)
   def __str__(self):
      return f'{self.bool}'
   def __getitem__(self):
      return self.bool
   def __setitem__(self, value):
      self.bool = value
   def Boolean(self, expression):
      if type(expression) == int or type(expression) == float or type(expression) == Number:
         if expresssion == 0:
            result = False
         else:
            result = True
      if expression == "NaN":
         result = False
      if type(expresssion) == str or type(expression) == String:
         if exression == "":
            result = False
         else:
            result = True
      if expression == "null":
         result = False
      if expression == "undefined":
         result = False
      return result
   def toString(self):
      return str(self.bool)
   def valueOf(self):
      if self.bool == True:
         return True
      else:
         return False
class Date:
   def __init__(self, time=time()):
      self.time = time
      #self.date
      #self.dateUTC
      #self.day
      #self.dayUTC
      #self.fullYear
      #self.fullYearUTC
      #self.hours
      #self.hoursUTC
      #self.milliseconds
      #self.millisecondsUTC
      #self.minutes
      #self.minutesUTC
      #self.month
      #self.monthUTC
      #self.seconds
      #self.secondsUTC
      self._tz = str(strftime('%Z%z'))
      self.timezoneOffset = self._getcurrenttzoffset()
   def __str__(self):
      #returns dayoftheweek month dayofmonth time timezone year
      pass
   def __repr__(self):
      return self.time
   def _getcurrenttzoffset(self):
      #Returns difference in minutes between local and UTC
      i1 = self._tz.find("-")
      if i1 == -1:
         i1 = self._tz.find("+")
         if i1 == -1:
            return 0
         else:
            signmult = 1
            l1 = self._tz.split("+")
      else:
         signmult = -1
         l1 = self._tz.split("-")
      l2 = wrap(l1[1],1)
      hours = int(l2.pop(0) + l2.pop(0))
      minutes = int(l2.pop(0) + l2.pop(0))
      return (hours * 60 + minutes) * signmult
   def Date():
      pass
   def getDate():
      pass
   def getDay():
      pass
   def getFullYear():
      pass
   def getHours():
      pass
   def getMilliseconds():
      pass
   def getMinutes():
      pass
   def getMonth():
      pass
   def getSeconds():
      pass
   def getTime():
      pass
   def getTimezoneOffset():
      pass
   def getUTCDate():
      pass
   def getUTCDay():
      pass
   def getUTCFullYear():
      pass
   def getUTCHours():
      pass
   def getUTCMilliseconds():
      pass
   def getUTCMinutes():
      pass
   def GetUTCMonth():
      pass
   def getUTCSeconds():
      pass
   def parse():
      pass
   def setDate():
      pass
   def setFullYear():
      pass
   def setHours():
      pass
   def setMilliseconds():
      pass
   def setMinutes():
      pass
   def setMonth():
      pass
   def setSeconds():
      pass
   def setTime():
      pass
   def setUTCDate():
      pass
   def setUTCFullYear():
      pass
   def setUTCHours():
      pass
   def setUTCMilliseconds():
      pass
   def setUTCMinutes():
      pass
   def setUTCMonth():
      pass
   def setUTCSeconds():
      pass
   def toDateString():
      pass
   def toJSON():
      pass
   def toLocaleDateString():
      pass
   def toLocaleString():
      pass
   def toLocaleTimeString():
      pass
   def toString():
      pass
   def toTimeString():
      pass
   def toUTCString():
      pass
   def UTC():
      pass
   def valueOf(self):
      return self.time
class DefinitionError(Exception):
   def __init__(self, message=""):
      self.error = message
def decodeURI():
   pass
def decodeURIComponent():
   pass
def encodeURI():
   pass
def encodeURIComponent():
   pass
class Error(Exception):
   def __init__(self, message=""):
      self.error = message
def escape(Str):
   """
   Converts the parameter to a string and encodes it in a URL-encoded format, where most nonalphanumeric characters are replaced with % hexadecimal sequences. When used in a URL-encoded string, the percentage symbol (%) is used to introduce escape characters, and is not equivalent to the modulo operator (%). 
   The following characters are not converted to escape sequences by the escape() function.
   0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@-_.*+/
   """
   tempdict1 = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '€', '\x81', '‚', 'ƒ', '„', '…', '†', '‡', 'ˆ', '‰', 'Š', '‹', 'Œ', '\x8d', 'Ž', '‘', '\x8F', '\x90', '’', '“', '”', '•', '–', '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '!', '\xa0', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']
   tempdict2 = ['%20', '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29', '*', '+', '%2C', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%3A', '%3B', '%3C', '%3D', '%3E', '%3F', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '%5B', '%5C', '%5D', '%5E', '_', '%60', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '%7B', '%7C', '%7D', '%7E', '%7F', '%80', '%81', '%82', '%83', '%84', '%85', '%86', '%87', '%88', '%89', '%8A', '%8B', '%8C', '%8D', '%8E', '%8f', '%90', '%91', '%92', '%93', '%94', '%95', '%96', '%97', '%98', '%99', '%9A', '%9B', '%9C', '%9D', '%9E', '%9F', '%A0', '%A1', '%A2', '%A3', '%A4', '%A5', '%A6', '%A7', '%A8', '%A9', '%AA', '%AB', '%AC', '%AD', '%AE', '%AF', '%B0', '%B1', '%B2', '%B3', '%B4', '%B5', '%B6', '%B7', '%B8', '%B9', '%BA', '%BB', '%BC', '%BD', '%BE', '%BF', '%C0', '%C1', '%C2', '%C3', '%C4', '%C5', '%C6', '%C7', '%C8', '%C9', '%CA', '%CB', '%CC', '%CD', '%CE', '%CF', '%D0', '%D1', '%D2', '%D3', '%D4', '%D5', '%D6', '%D7', '%D8', '%D9', '%DA', '%DB', '%DC', '%DD', '%DE', '%DF', '%E0', '%E1', '%E2', '%E3', '%E4', '%E5', '%E6', '%E7', '%E8', '%E9', '%EA', '%EB', '%EC', '%ED', '%EE', '%EF', '%F0', '%F1', '%F2', '%F3', '%F4', '%F5', '%F6', '%F7', '%F8', '%F9', '%FA', '%FB', '%FC', '%FD', '%FE', '%FF']
   tempString1 = str(Str)
   templist = wrap(tempString1, 1)
   tempString2 = String()
   for i in range(0,len(templist)):
      try:
         tempi = tempdict1.index(templist[i])
      except:
         tempi = -1
      if tempi == -1:
         tempString2 += ""
      else:
         tempString2 += tempdict2[tempi]
   return tempString2
class EvalError(Exception):
   def __init__(self, message=""):
      self.error = message
class Int:
   MAX_VALUE = 2147483647
   MIN_VALUE = -2147483648
   def __init__(self, value):
      self.value = self.int(value)
   def __str__(self):
      return f'{self.value}'
   def __getitem__(self):
      return self.value
   def __setitem__(self, value):
      self.value = self.int(value)
   def __add__(self, value):
      return Int(self.value + self.int(value))
   def __sub__(self, value):
      return Int(self.value - self.int(value))
   def __mul__(self, value):
      return Int(self.value * self.int(value))
   def __truediv__(self, value):
      if value == 0:
         if self.value == 0:
            return Number(Number.NaN)
         elif self.value > 0:
            return Number(Number.POSITIVE_INFINITY)
         elif self.value < 0:
            return Number(Number.NEGATIVE_INFINITY)
      else:
         try:
            return Int(self.value / self.int(value))
         except:
            raise TypeError("Can not divide Int by " + f'{type(value)}')
   def __float__(self):
      return float(self.value)
   def __int__(self):
      return self.value
   def int(self, value):
      if type(value) == int or type(value) == Int:
         return value
      elif type(value) == float or type(value) == Number:
         return int(value)
      elif type(value) == str or type(value) == String:
         try:
            return int(value)
         except:
            raise TypeError("Can not convert " + str(value) + " to integer")
      else:
         raise TypeError("Can not convert " + str(value) + " to integer")
   def toExponential(self, fractionDigits):
      if fractionDigits < 0 or fractionDigits > 20:
         raise Exception("RangeError: fractionDigits is outside of acceptable range")
      else:
         tempString1 = str(self.value)
         templist = wrap(tempString1,1)
         if templist[0] == "-":
            templist.pop(0)
            exponent = len(templist) - 1
            tempString2 = "-" + templist.pop(0) + "."
         else:
            exponent = len(templist) - 1
            tempString2 = templist.pop(0) + "."
         if exponent == 0:
            return self.value
         else:
            i = 0
            while i < fractionDigits:
               tempString2 += templist.pop(0)
               i += 1
            return tempString2 + "e+" + str(exponent)
   def toFixed(self,fractionDigits):
      if fractionDigits < 0 or fractionDigits > 20:
         raise Exception("RangeError: fractionDigits is outside of acceptable range")
      else:
         tempString = str(self.value)
         if fractionDigits == 0:
            return tempString
         else:
            tempString += "."
            i = 0
            while i < fractionDigits:
               tempString += "0"
               i += 1
            return tempString
   def toPrecision():
      pass
   def toString(self, radix=10):
      #!
      if radix > 36 or radix < 2:
         pass
      else:
         return base_repr(self.value, base=radix)
   def valueOf(self):
      return self.value
def isFinite(num):
   if num == inf or num == NINF:
      return False
   else:
      return True
def isNaN(num):
   if num == nan:
      return True
   else:
      return False
class Math:
   E = 2.71828182845905
   LN10 = 2.302585092994046
   LN2 = 0.6931471805599453
   LOG10E = 0.4342944819032518
   LOG2E = 1.442695040888963387
   PI = 3.141592653589793
   SQRT1_2 = 0.7071067811865476
   SQRT2 = 1.4142135623730951
   def abs(val):
      return abs(val)
   def acos(val):
      return m.acos(val)
   def asin(val):
      return m.asin(val)
   def atan(val):
      return m.atan(val)
   def atan2(y, x):
      return m.atan2(y,x)
   def ceil(val):
      return m.ceil(val)
   def cos(angleRadians):
      return m.cos(angleRadians)
   def exp(val):
      return m.exp(val)
   def floor(val):
      return m.floor(val)
   def log(val):
      return m.log(val)
   def max(*values):
      return max(values)
   def min(*values):
      return min(values)
   def pow(base, pow):
      return m.pow(base,pow)
   def random():
      return r.random()
   def round(val):
      return round(val)
   def sin(angleRadians):
     return m.sin(angleRadians)
   def sqrt(val):
      return m.sqrt(val)
   def tan(angleRadians):
      return m.tan(angleRadians)
class Number:
   MAX_VALUE = 1.79e308
   MIN_VALUE = 5e-324
   NaN = NaN()
   NEGATIVE_INFINITY = NInfinity()
   POSITIVE_INFINITY = Infinity()
   def __init__(self, num):
      self.number = self.Number(num)
   def __str__(self):
      if self.number == self.NaN or self.number == self.POSITIVE_INFINITY or self.number == self.NEGATIVE_INFINITY:
         return str(self.number)
      tempString = str(self.number)
      templist = tempString.split(".")
      if templist[1] == "0":
         return f'{int(templist[0])}'
      else:
         return f'{self.number}'
   def __getitem__(self):
      return self.number
   def __setitem__(self, value):
      self.number = value
   def __add__(self, value):
      try:
         return Number(self.number + float(value))
      except ValueError:
         raise TypeError("can not add " + f'{type(value)}' + " to Number")
   def __sub__(self, value):
      try:
         return Number(self.number - float(value))
      except ValueError:
         raise TypeError("can not subtract " + f'{type(value)}' + " from Number")
   def __mul__(self, value):
      try:
         return Number(self.number * float(value))
      except ValueError:
         raise TypeError("can not multiply Number by " + f'{type(value)}')
   def __truediv__(self, value):
      if value == 0:
         if self.number == 0:
            return Number(self.NaN)
         elif self.number > 0:
            return Number(self.POSITIVE_INFINITY)
         elif self.number < 0:
            return Number(self.NEGATIVE_INFINITY)
      else:
         try:
            return Number(self.number / float(value))
         except:
            raise TypeError("Can not divide Number by " + f'{type(value)}')
   def __float__(self):
      return float(self.number)
   def __int__(self):
      return int(self.number)
   def Number(self, expression):
      if expression == self.NEGATIVE_INFINITY:
         return self.NEGATIVE_INFINITY
      elif expression == self.POSITIVE_INFINITY:
         return self.POSITIVE_INFINITY
      elif type(expression) == int or type(expression) == float or type(expression) == Number:
         return expression
      elif expression == "undefined":
         return self.NaN
      elif expression == "null":
         return 0.0
      elif expression == self.NaN:
         return self.NaN
      elif type(expression) == bool or type(expression) == Boolean:
         if expression == True:
            return 1.0
         else:
            return 0.0
      elif type(expression) == str or type(expression) == String:
         if expression == "":
            return 0.0
         else:
            try:
               return float(expression)
            except:
               return self.NaN
   def toExponential(self):
      pass
   def toFixed(self):
      pass
   def toPrecision():
      pass
   def toString(self, radix=10):
      #!
      return str(self.number)
   def valueOf(self):
      return self.number
def parseFloat():
   pass
def parseInt():
   pass
class RangeError(Exception):
   def __init__(self, message=""):
      self.error = message
class ReferenceError(Exception):
   def __init__(self, message=""):
      self.error = message
class RegExp:
   pass
class SecurityError(Exception):
   def __init__(self, message=""):
      self.error = message
class String:
   def __init__(self, value=""):
      self.string = self.String(value)
   def __str__(self):
      return self.string
   def __getitem__(self, item={}):
      if item == {}:
         return self.string
      else:
         return self.string[item]
   def __setitem__(self, value):
      self.string = value
   def __len__(self):
      return len(self.string)
   def __add__(self, value):
      return String(self.string + self.String(value))
   def __int__(self):
      return int(self.string)
   def __float__(self):
      return float(self.string)
   def length(self):
      return len(self.string)
   def String(self, expression):
      if type(expression) == str:
         return expression
      elif type(expression) == String:
         return expression.string
      elif type(expression) == bool:
         if expression == True:
            return "true"
         elif expression == False:
            return "false"
      elif expression == nan:
         return "NaN"
      elif type(expression) == Array or type(expression) == Boolean or type(expression) == Number:
         return expression.toString()
      else:
         return str(expression)
   def charAt(self, index=0):
      if index < 0 or index > len(self.string) - 1:
         return ""
      else:
         return self.string[index]
   def charCodeAt(self, index=0):
      if index < 0 or index > len(self.string) - 1:
         return nan
      else:
         return r'\u{:04X}'.format(ord(self.string[index]))
   def concat(self, *args):
      tempString = self.string
      for i in range(0, len(args)):
         tempString += self.String(args[i])
      return tempString
   def fromCharCode():
      pass
   def indexOf(self, val, startIndex=0):
      return self.string.find(val, startIndex)
   def lastIndexOf(self, val, startIndex={}):
      tempInt = len(self.string) - 1
      if startIndex == {} or startIndex > tempInt:
         return self.string.rfind(val,0,tempInt)
      else:
         return self.string.rfind(val,0,startIndex)
   def localeCompare():
      pass
   def match():
      pass
   def replace():
      pass
   def search():
      pass
   def slice():
      pass
   def split():
      pass
   def substr(self, startIndex=0, Len={}):
      tempInt = len(self.string)
      tempString1 = wrap(self.string,1)
      if startIndex > tempInt - 1:
         raise RangeError("startIndex is outside of the string")
      if startIndex < 0 and abs(startIndex) > tempInt:
         raise RangeError("startIndex is outside of the string")
      if Len == {}:
         length = tempInt
      else:
         length = Len
      if startIndex < 0:
         tempIndex = tempInt - abs(startIndex)
      else:
         tempIndex = startIndex
      i = tempIndex
      tempString2 = ""
      if tempIndex + length >= tempInt:
         while i < tempInt:
            tempString2 += tempString1[i]
            i += 1
      else:
         while i < tempIndex + length:
            tempString2 += tempString1[i]
            i += 1
      return tempString2
   def substring(self, startIndex=0, endIndex={}):
      tempInt = len(self.string)
      si = startIndex
      ei = endIndex
      tempString = String()
      if si < 0:
         si = 0
      if ei != {}:
         if ei < 0:
            ei = 0
      else:
         ei = tempInt
      if si > ei:
         temp = si
         si = ei
         ei = temp
      for i in range(si,ei):
         tempString += self.string[i]
      return tempString
   def toLocaleLowerCase(self):
      return self.toLowerCase()
   def toLocaleUpperCase(self):
      return self.toUpperCase()
   def toLowerCase(self):
      return self.string.lower()
   def toUpperCase(self):
      return self.string.upper()
   def valueOf(self):
      return self.string
class SyntaxError(Exception):
   def __init__(self, message=""):
      self.error = message
def trace(*args):
   output = ""
   for i in range(0, len(args)):
      if len(args) == 1:
         output = str(args[0])
      else:
         if i == len(args) - 1:
            output += str(args[i])
         else:
            output += str(args[i]) + " "
   print(output)
class TypeError(Exception):
   def __init__(self, message=""):
      self.error = message
class uint:
   pass
def unescape(Str):
   """
   Evaluates the parameter str as a string, decodes the string from URL-encoded format (converting all hexadecimal sequences to ASCII characters), and returns the string. 
   """
   tempdict1 = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '€', '\x81', '‚', 'ƒ', '„', '…', '†', '‡', 'ˆ', '‰', 'Š', '‹', 'Œ', '\x8d', 'Ž', '‘', '\X8f', '\x90', '’', '“', '”', '•', '–', '—', '˜', '™', 'š', '›', 'œ', 'ž', 'Ÿ', '!', '\xa0', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']
   tempdict2 = ['%20', '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29', '%2A', '%2B', '%2C', '%2D', '%2E', '%2F', '%30', '%31', '%32', '%33', '%34', '%35', '%36', '%37', '%38', '%39', '%3A', '%3B', '%3C', '%3D', '%3E', '%3F', '%40', '%41', '$42', '%43', '%44', '%45', '%46', '%47', '%48', '%49', '%4A', '%4B', '%4C', '%4D', '%4E', '%4F', '%50', '%51', '%52', '%53', '%54', '%55', '%56', '%57', '%58', '%59', '%5A', '%5B', '%5C', '%5D', '%5E', '%5F', '%60', '%61', '%62', '%63', '%64', '%65', '%66', '%67', '%68', '%69', '%6A', '%6B', '%6C', '%6D', '%6E', '%6F', '%70', '%71', '%72', '%73', '%74', '%75', '%76', '%77', '%78', '%79', '%7A', '%7B', '%7C', '%7D', '%7E', '%7F', '%80', '%81', '%82', '%83', '%84', '%85', '%86', '%87', '%88', '%89', '%8A', '%8B', '%8C', '%8D', '%8E', '%8f', '%90', '%91', '%92', '%93', '%94', '%95', '%96', '%97', '%98', '%99', '%9A', '%9B', '%9C', '%9D', '%9E', '%9F', '%A0', '%A1', '%A2', '%A3', '%A4', '%A5', '%A6', '%A7', '%A8', '%A9', '%AA', '%AB', '%AC', '%AD', '%AE', '%AF', '%B0', '%B1', '%B2', '%B3', '%B4', '%B5', '%B6', '%B7', '%B8', '%B9', '%BA', '%BB', '%BC', '%BD', '%BE', '%BF', '%C0', '%C1', '%C2', '%C3', '%C4', '%C5', '%C6', '%C7', '%C8', '%C9', '%CA', '%CB', '%CC', '%CD', '%CE', '%CF', '%D0', '%D1', '%D2', '%D3', '%D4', '%D5', '%D6', '%D7', '%D8', '%D9', '%DA', '%DB', '%DC', '%DD', '%DE', '%DF', '%E0', '%E1', '%E2', '%E3', '%E4', '%E5', '%E6', '%E7', '%E8', '%E9', '%EA', '%EB', '%EC', '%ED', '%EE', '%EF', '%F0', '%F1', '%F2', '%F3', '%F4', '%F5', '%F6', '%F7', '%F8', '%F9', '%FA', '%FB', '%FC', '%FD', '%FE', '%FF']
   tempString1 = str(Str)
   templist = wrap(tempString1,1)
   tempString2 = String()
   while len(templist) > 0:
      tempString3 = ""
      if templist[0] == "%":
         for i in range(0,3):
            tempString3 += templist.pop(0)
         tempi = tempdict2.index(tempString3)
         tempString2 += tempdict1[tempi]
      else:
         tempString2 += templist.pop(0)
   return tempString2
class URIError(Exception):
   def __init__(self, message=""):
      self.error = message
class Vector:
   pass
class VerifyError(Exception):
   def __init__(self, message=""):
      self.error = message
