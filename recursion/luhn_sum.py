#介绍：银行卡号从右往左，每第二个数字翻倍，若其大于9，则变为十位数字和个位数字之和，再与其余数字相加，其和必为10的倍数

def split(n):
  #用于分离整数n的个位数和其余位数
  return n//10,n%10

def sum_digits(n):
  #当n大于9时，令其等于个位数加其余位数
  if n<10: return n
  return n//10+n%10
  
def luhn_sum(n):
  if n<10: return n 
  all_nolast,last=split(n)
  return luhn_sum_double(all_nolast)+last

def luhn_sum_double(n):
  all_nolast,last=split(n)
  if n<10: return sum_digits(2*last)
  return luhn_sum(all_nolast)+sum_digits(2*last)


