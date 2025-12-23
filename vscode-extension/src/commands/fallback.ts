// Shared Dart fallbacks
function sanitize(s: string): string {
  return (s || "").replace(/[^A-Za-z0-9_]/g, "");
}

export function toSnakeCase(name: string): string {
  return name.replace(/(?<!^)([A-Z])/g, "_$1").toLowerCase();
}

function pascalCase(s: string): string {
  return sanitize(s)
    .split(/[_\s]+/)
    .filter(Boolean)
    .map(p => p[0].toUpperCase() + p.slice(1))
    .join("") || "Unnamed";
}

function lowerCamelCase(s: string): string {
  const p = pascalCase(s);
  return p[0].toLowerCase() + p.slice(1);
}

// Enum
export function enumFallback(name: string, values?: string[]): string {
  const enumName = pascalCase(name);
  const items =
    values && values.length
      ? values.map(v => lowerCamelCase(v))
      : ["value1", "value2", "value3"];

  return `enum ${enumName} {\n${items.map(v => `  ${v},`).join("\n")}\n}\n`;
}

// Model

export function modelFallback(name: string): string {
  const className = pascalCase(name);
  return `class ${className} {
  const ${className}();
}
`;
}

// Repository

export function repositoryFallback(name: string, entity?: string): string {
  const repo = pascalCase(name);
  const ent = entity ? pascalCase(entity) : "Object";

  return `class ${repo} {
  const ${repo}();

  Future<List<${ent}>> fetchAll() async {
    return [];
  }
}
`;
}

// Screen
export function screenFallback(name: string): string {
  const screen = pascalCase(name);

  return `import 'package:flutter/material.dart';

class ${screen} extends StatelessWidget {
  const ${screen}({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Text('${screen}'),
      ),
    );
  }
}
`;
}

// Widget

export function widgetFallback(name: string, stateful: boolean): string {
  const widget = pascalCase(name);

  if (!stateful) {
    return `import 'package:flutter/material.dart';

class ${widget} extends StatelessWidget {
  const ${widget}({super.key});

  @override
  Widget build(BuildContext context) {
    return const SizedBox();
  }
}
`;
  }

  return `import 'package:flutter/material.dart';

class ${widget} extends StatefulWidget {
  const ${widget}({super.key});

  @override
  State<${widget}> createState() => _${widget}State();
}

class _${widget}State extends State<${widget}> {
  @override
  Widget build(BuildContext context) {
    return const SizedBox();
  }
}
`;
}