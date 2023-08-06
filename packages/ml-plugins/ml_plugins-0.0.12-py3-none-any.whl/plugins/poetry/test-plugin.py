from metaflow.decorators import step
from metaflow.flowspec import FlowSpec
from metaflow.includefile import IncludeFile
from plugin import poetry


class IncludeFileFlow(FlowSpec):
    data = IncludeFile('data', 
                       default='config.toml')
    @poetry()
    @step
    def show(self):
        self.next(self.end)

    @step
    def start(self):
        print(self.data)
        self.next(self.show)

    @step
    def end(self):
        import fasttext
        print('Finished reading the data!')

if __name__ == '__main__':
    IncludeFileFlow()
