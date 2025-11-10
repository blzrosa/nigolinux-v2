from typing import Iterable, Optional, Generic, TypeVar, Iterator
import sys
import time

T = TypeVar('T')

class NoneIter(Iterator[None]):
    def __iter__(self) -> Iterator[None]:
        return self
    
    def __next__(self) -> None:
        return None

def clear() -> None:
    print(end='\r\x1b[K', file=sys.stderr, flush=True)

class ProgressBar(Generic[T]):
    def __init__(
            self, iterable: Iterable[T], 
            labels: Optional[Iterable[str]] = None, 
            title: Optional[str] = 'Progress'
            ) -> None:
        self.iterable: Iterable[T] = iterable
        self.iterator: Iterator[T] = iter(self.iterable)
        self.labels: Optional[Iterable[str]] = labels
        self.label_iterator: Iterator[str] | Iterator[None] = iter(self.labels) if self.labels else NoneIter()
        self.title: Optional[str] = title
        size: Optional[int] = len(iterable) if hasattr(iterable, '__len__') else None # type: ignore
        if size is not None:
            self.__len__: int = size
            self.total_size: int = size
        self.actual_iter: int = 0
        self.done: bool = False
        self.current_label: Optional[str] = None
    
    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        try:
            self._print_progress()
            item: T = next(self.iterator)
            try:
                self.current_label = next(self.label_iterator)
            except StopIteration:
                self.label_iterator = NoneIter()
                self.current_label = None
            self.actual_iter += 1
            return item
        except StopIteration:
            self.done = True
            self._print_progress()
            raise
    
    def __repr__(self) -> str:
        total: Optional[int] = self.total_size if hasattr(self, 'total_size') else None
        if total:
            return f'<TypedProgressBar {self.actual_iter} of {total}>'
        else: 
            return f'<TypedProgressBar {self.actual_iter} of unknown>'
    
    @property
    def progress_percentage(self) -> Optional[float]:
        total: Optional[int] = self.total_size if hasattr(self, 'total_size') else None
        if total is not None:
            if total == 0:
                return 100.0
            return float(self.actual_iter / total) * 100
        return None

    def __get_progress_character(self, digit: int) -> str:
        if digit == 0:
            return '▁'
        if digit == 1:
            return '▂'
        if digit <= 3:
            return '▃'
        if digit == 4:
            return '▄'
        if digit == 5:
            return '▅'
        if digit <= 7:
            return '▆'
        if digit <= 9:
            return '▇'
            
        return '█'

    @property
    def progress_bar(self) -> str:
        if self.done:
            return '█' * 10
        progress_percentage: Optional[float] = self.progress_percentage
        progress_floor: int = int(progress_percentage) if progress_percentage else 0
        if progress_floor >= 100:
            return '█' * 10
        ten: int = progress_floor // 10
        unit: int = progress_floor % 10
        return f'{'█' * ten}{self.__get_progress_character(unit)}{'▁'*(9-ten)}'



    def _print_progress(self) -> None:
        end_seq: str = '\x1b[K'
        if self.done:
            clear()
            return
        
        total: Optional[int] = self.total_size if hasattr(self, 'total_size') else None
        
        label_str = f', item = {self.current_label}' if self.current_label is not None else ''

        if total is not None:
            perc_str = f'[{self.progress_percentage:6.2f}%]' if self.progress_percentage is not None else '[ ?.?%]'
            
            print(
                f'\r\x1b[K{self.title}: {self.progress_bar} {self.actual_iter :{len(str(total))}} / {total} {perc_str}{label_str}', 
                end=end_seq,
                file=sys.stderr, 
                flush=True
            )
        else:
            print(
                f'\r\x1b[K{self.title}: {self.actual_iter} processed{label_str}', 
                end=end_seq,
                file=sys.stderr, 
                flush=True
            )

def TypedProgressBar(
    iterable: Iterable[T], 
    labels: Optional[Iterable[str]] = None, 
    title: Optional[str] = 'Progress'
) -> ProgressBar[T]:
    return ProgressBar(iterable, labels, title)

if __name__ == '__main__':
    labels = list(str(x) for x in range(50))
    iterations = list(range(100))
    for _ in TypedProgressBar(iterations, labels=labels):
        time.sleep(0.01)
    
    x: int = 0
    for _ in TypedProgressBar(NoneIter(), labels=labels):
        if x >= 100:
            clear()
            break
        x += 1
        time.sleep(0.01)