import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { PanelLeftClose } from "lucide-react";
import { Overview } from "./overview";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onDeleteChat?: (chatId: string) => void;
  onQuestionClick?: (question: string) => void;
  className?: string;
}

export function Sidebar({ isOpen, onClose, onQuestionClick, className }: SidebarProps) {

  return (
    <div
      className={cn(
        "flex flex-col h-full bg-secondary text-secondary-foreground transition-all duration-300 ease-in-out",
        isOpen ? "w-full md:w-80 p-4" : "w-0",
        "overflow-hidden",
        className
      )}
    >
      {isOpen && (
        <>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Suggestions</h2>
            <Button variant="ghost" size="icon" onClick={onClose} className="md:hidden">
              <PanelLeftClose className="h-5 w-5" />
            </Button>
          </div>
          <Overview onQuestionClick={onQuestionClick ?? (() => {})} />
        </>
      )}
    </div>
  );
}
