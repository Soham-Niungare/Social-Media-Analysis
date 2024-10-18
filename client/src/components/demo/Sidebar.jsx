export function Sidebar() {
  return (
    <>
      <div className="flex h-[100%] flex-col justify-between border-e bg-white ml-2">
        <div className="px-4 py-6 ">
          <span className="grid place-content-center rounded-lg text-teal-600 px-2 font-bold text-2xl shadow-[rgba(0,_0,_0,_0.24)_0px_3px_8px]">
            TweetLense
          </span>

          <ul className="mt-6 space-y-1">
            <li>
              <a
                href="#"
                className="block rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700"
              >
                About
              </a>
            </li>

            <li>
              <a
                href="#"
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700"
              >
                Blog
              </a>
            </li>

            <li>
              <a
                href="#"
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700"
              >
                Contact
              </a>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
}
