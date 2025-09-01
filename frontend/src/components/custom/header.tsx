import { ThemeToggle } from "./theme-toggle";
import { Button } from "../ui/button";
import { PanelLeftOpen } from "lucide-react";

interface HeaderProps {
  onToggleSidebar: () => void;
}

export function Header({ onToggleSidebar }: HeaderProps) {
  return (
    <header className="flex items-center justify-between p-4 border-b bg-background">
      <Button variant="ghost" size="icon" onClick={onToggleSidebar}>
        <PanelLeftOpen className="h-5 w-5" />
        <span className="sr-only">Toggle Suggestions</span>
      </Button>
      <h1 className="text-xl font-bold">Neo4j Chat</h1>
      <ThemeToggle />
    </header>
  );
}