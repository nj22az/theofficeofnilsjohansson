
import { useLocation } from "react-router-dom";
import { useRef } from "react";
import SidebarNav from "./SidebarNav";

const Sidebar = () => {
  const location = useLocation();
  const animationContainerRef = useRef<HTMLDivElement>(null);

  const handleLinkClick = () => {
    if (window.innerWidth < 768) {
      const sidebar = document.querySelector('aside');
      sidebar?.classList.add('-translate-x-full');
    }
  };

  return (
    <aside ref={animationContainerRef} className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 border-r border-border bg-background/80 backdrop-blur-md -translate-x-full md:translate-x-0 transition-transform duration-300 ease-in-out z-40">
      <SidebarNav onLinkClick={handleLinkClick} />
      <div className="absolute bottom-0 left-0 right-0 p-4 text-center text-sm text-muted-foreground border-t border-border">
        © 2025 Nils Johansson. All rights reserved.
      </div>
    </aside>
  );
};

export default Sidebar;
