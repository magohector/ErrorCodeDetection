class WhileLoopFinder(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code.splitlines()
        self.functions_with_while = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        original_current_function = self.current_function
        self.current_function = {
            "function_name": node.name,
            "has_while_loop": False,
            "pre_while_code_lines": [],
            "while_loops": []
        }

        function_start_line = node.lineno - 1
        function_end_line = (node.end_lineno if hasattr(node, 'end_lineno') else len(self.source_code))
        function_lines = self.source_code[function_start_line:function_end_line]

        found_while = False
        for stmt in node.body:
            if isinstance(stmt, ast.While):
                self.current_function["has_while_loop"] = True
                found_while = True
                try:
                    while_condition = ast.unparse(stmt.test).strip()
                    print("OK condition")
                except AttributeError:
                    print("Error al obtener la condición del while")
                try:
                    while_body_code = ast.unparse(ast.Module(body=stmt.body, type_ignores=[])).strip()
                    print("Ok body")
                except AttributeError:
                    print("Error al obtener el código del cuerpo del while")

                self.current_function["while_loops"].append({
                    "condition": while_condition,
                    "body_code": while_body_code
                })
            elif not found_while:
                start_line = stmt.lineno - 1
                end_line = (stmt.end_lineno if hasattr(stmt, 'end_lineno') else stmt.lineno)
                self.current_function["pre_while_code_lines"].extend(self.source_code[start_line:end_line])
            self.generic_visit(stmt)

        if self.current_function["has_while_loop"]:
            last_while_end_line = None
            if self.current_function["while_loops"]:
                last_while_node = next((node for node in reversed(node.body) if isinstance(node, ast.While)), None)
                if last_while_node and hasattr(last_while_node, 'end_lineno'):
                    last_while_end_line = last_while_node.end_lineno
            post_while_code_lines = []
            if last_while_end_line:
                function_indent = len(self.source_code[node.lineno - 1]) - len(self.source_code[node.lineno - 1].lstrip())
                for line in self.source_code[last_while_end_line:function_end_line]:
                    if line.startswith(self.source_code[node.lineno - 1][:function_indent] + "    "):
                        post_while_code_lines.append(line[function_indent + 4:])
                    else:
                        post_while_code_lines.append(line[function_indent:])
            self.current_function["post_while_code_lines"] = "\n".join(post_while_code_lines).strip()
            self.current_function["pre_while_code_lines"] = "\n".join(self.current_function["pre_while_code_lines"]).strip()
            self.functions_with_while.append(self.current_function)

        self.current_function = original_current_function

## Use Class
def DGries_states(solution):
  try:
    # Crear el AST
    tree = ast.parse(solution)
    # Recorrer el AST con nuestro visitante
    finder = WhileLoopFinder(solution)
    finder.visit(tree)
    for func_info in finder.functions_with_while:
      initial_state=func_info["pre_while_code_lines"] if func_info["pre_while_code_lines"] else False
      end_state=""
      transformation_state=""
      for j, wl in enumerate(func_info["while_loops"]):
          end_state=wl["condition"]
          transformation_state=wl["body_code"]

      if not initial_state:
        initial_state=transformation_state
      return initial_state,transformation_state,end_state
  except Exception as error:
    return "Exception:"+str(error),"Exception:"+str(error),"Exception:"+str(error)
