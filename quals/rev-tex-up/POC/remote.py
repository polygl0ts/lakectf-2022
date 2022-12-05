
print("So what word did you do? ", end='')
line = input().strip()
flag = """
Fine here's my part of the report:
\\newcommand{\\flag}{
	\char\dataa
	\char\datab
	\char\datac
	\char\datad
}"""
if line=="wass_up":
    print(flag)
else:
    print("What's that bullshit? Do your work") # Should I use nonsense instead
