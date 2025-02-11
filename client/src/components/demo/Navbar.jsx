// import { Button } from "../ui/button";
// import { RxHamburgerMenu } from "react-icons/rx";

// export function Navbar() {
//   return (
//     <>
//       <nav className="bg-white shadow-md">
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//           <div className="flex justify-between h-16">
//             <div className="flex-shrink-0 flex items-center">
//               <a href="/" className="text-2xl font-bold text-blue-600">
//                 InsightPulse
//               </a>
//             </div>
//             <div className="items-center hidden md:flex">
//               <Button variant="ghost" className="md:mr-4">
//                 Sentiment Analysis
//               </Button>
//               <Button variant="ghost" className="md:mr-4">
//                 Trend Identification
//               </Button>
//               <Button>Get Started</Button>
//             </div>
//             <div className="text-xl text-black md:hidden flex items-center">
//               <RxHamburgerMenu />
//             </div>
//           </div>
//         </div>
//       </nav>
//     </>
//   );
// }



import { Button } from "../ui/button";
import { RxHamburgerMenu } from "react-icons/rx";

export function Navbar({ scrollToSection, sentimentRef, trendRef }) {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex-shrink-0 flex items-center">
            <a href="/" className="text-2xl font-bold text-blue-600">
              InsightPulse
            </a>
          </div>
          <div className="items-center hidden md:flex">
            <Button variant="ghost" className="md:mr-4" onClick={() => scrollToSection(sentimentRef)}>
              Sentiment Analysis
            </Button>
            <Button variant="ghost" className="md:mr-4" onClick={() => scrollToSection(trendRef)}>
              Trend Identification
            </Button>
            <Button>Get Started</Button>
          </div>
          <div className="text-xl text-black md:hidden flex items-center">
            <RxHamburgerMenu />
          </div>
        </div>
      </div>
    </nav>
  );
}
