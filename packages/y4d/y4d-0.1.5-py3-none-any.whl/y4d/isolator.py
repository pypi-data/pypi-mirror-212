import typer
from y4d import codeParser as codeParser
from y4d import commentController as commentController

app = typer.Typer()



@app.command("f")
def isolateFunction(source: str  = typer.Argument(..., help="The source code that the function will be isolated from (.cpp/.h)"),
                    destination: str  = typer.Argument(..., help="The destination code where the function will be embedded or replaced (.cpp/.h)"),
                    prototype: str  = typer.Argument(..., help="The function prototype: return-type function-name parameters-types. In the case of member functions return-type class-name::function-name parameters-types. Example: int test(int, string). Must put them in quotations when using CLI.")):
    """
    Isolates out a function, the function will be taken from source and replace the one in destination or add one.
    """
    
    findFunction = codeParser.positions(source,"function", prototype)
    if findFunction == ["error"]:
        return
    if findFunction == []:
        print("Warning: Function doesn't exist in " + source +" file")
        return 
    
    # Open the source file and read its contents
    with open(source, "r") as source_file:
        lines = source_file.readlines() 
    
    #check if its a member function and parent class exists in destination file 
    if findFunction[2] != "function" and findFunction[2] != "template_function" and findFunction[2] != "main":
        parent_class = prototype.split("::")[0].strip().split(" ")[-1]
        findClass = codeParser.positions(destination, "class", "class " + parent_class)
        if findClass == ["error"]:
            return
        if findClass == []:
            findClass = codeParser.positions(destination, "struct", "struct " + parent_class)
            if findClass == ["error"]:
                return
            if findClass == []:
                print("Warning: Parent Class doesn't exist in " +destination +" file")
                return 
        class_end = findClass[1]
        #fixing protoype
        if findFunction[2] == "constructor" or findFunction[2] == "destructor":
            forward_implementation = prototype.split("::")[1]
        else:
            forward_implementation = prototype.split(parent_class)[0] + prototype.split(parent_class)[1]
            forward_implementation = forward_implementation.split("::")[0] + forward_implementation.split("::")[1]
    
    #commenting out the function in destination file
    commentController.CommentOutFunction(destination, prototype, 1, destination)
    
    #case: forward declaration or memebr functions implemented outside a class
    i=0
    if len(findFunction) > 4:
        i=4
    start_line = findFunction[i+0]
    end_line = findFunction[i+1]
    
    # Extract the lines you want to copy
    implementation = lines[start_line - 1:end_line]
    
    # Open the destination file and insert the copied lines at the appropriate position
    with open(destination, "r") as destination_file:
        lines = destination_file.readlines()
    #functions insertion
    if findFunction[2] == "function" or findFunction[2] == "template_function":
        lines = [prototype +";\n"]+ lines[0:] + ['\n'] + implementation  
    elif findFunction[2] == "main":
        lines = lines[0:] + ['\n'] + implementation  
    #member functions insertion 
    else:
        #if function implemented outside the class 
        if  i == 4:
            lines = lines[0: class_end-1] + [findFunction[i+3] + ": "] + [forward_implementation + ";\n"] + lines[class_end-1: ] +['\n']+ implementation 
        #if function implemented inside the class
        else:
            lines = lines[0: class_end-1] + [findFunction[i+3] + ": "] + implementation + ["\n"] + lines[class_end-1: ]
       
    # Write the modified lines to the destination file
    with open(destination, "w") as destination_file:
        destination_file.writelines(lines)



@app.command("c")
def isolateClass(
    source: str  = typer.Argument(..., help="The source code that the function will be isolated from (.cpp/.h)"), 
    destination: str  = typer.Argument(..., help="The destination code where the function will be embedded or replaced (.cpp/.h)"), 
    prototype: str  = typer.Argument(..., help="The class prototype: class class-name. Example: class test. Must put them in quotations when using CLI."),
    all: str  = typer.Option("f", "-all", help="If t this will isolate the class with all its children classes, if c this will isolate the class itself without any member function implemented outside the class,if f this will isolate the class with its member functions implemented outside the class. Takes c, t, or f. Default value is f.")):
    """
    Isolates out a class, the class will be taken from source and replace the one in destination or add one.
    """
    if all.lower() not in ["f","t", "c"]:
        print("Invalid input for -all")
        return False
    
    option =1
    if all == "t":
        option = 0
    elif all == "c":
        option = -1
    type = prototype.split(" ")[0]
    position = codeParser.positions(source, type, prototype, option)
    
    if position == ["error"]:
        return
    
    #checking if class exists in source code
    if position == []:
        print("Class not found in " + source)
        return
    
    with open(source, "r") as source_file:
        lines = source_file.readlines()
        
    n = len(position)
    things = []
    for i in range(0, int(n), 4): 
        if position[i+2] == type:
            class_start = position[i]
            class_end = position[i+1]
        start_line = position[i]
        end_line = position[i+1]
        #functions implemented outside a class
        if start_line <= class_start or end_line >= class_end:
            things += lines[start_line - 1:end_line]
    
    #checking if class already exists in destination code and commenting it out
    class_position = codeParser.positions(destination, type, prototype, 1)
    if class_position == ["error"]:
        return
    commentController.CommentOutClass(destination, prototype, all, 1, destination)
    
    with open(destination, "r") as destination_file:
        lines = destination_file.readlines()
        
        #if class doesnt exist in destination.cpp, the isolated class will be added at the end of the code.
        if class_position == []:
            lines =  lines +  ["\n"]  + things
        #if class exists in destination.cpp, it will be replaced by the isolated class.
        else:
            lines =  lines[0: class_position[0]-1] + things +  ["\n"] + lines[class_position[0]-1: ]
    
    
    
    # Write the modified lines to the destination file
    with open(destination, "w") as destination_file:
        destination_file.writelines(lines)



@app.callback()
def main():
    """
    Allows the user to copy a given function or class from the source code file into the destination code file and replaces. It consists of two parts, IsolateFunction and IsolateClass.\n\n
    For more information about each tool simply add the command you need followed by --help, for example:\n\n isolate f --help
    """



if __name__ == "__main__":
    app()
